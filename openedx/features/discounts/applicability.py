# -*- coding: utf-8 -*-
"""
Contains code related to computing discount percentage
and discount applicability.

WARNING:
Keep in mind that the code in this file only applies to discounts controlled in the lms like the first purchase offer,
not other discounts like coupons or enterprise/program offers configured in ecommerce.

"""


from datetime import datetime, timedelta

import pytz
from crum import get_current_request, impersonate
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from edx_toggles.toggles import WaffleFlag, WaffleFlagNamespace

from common.djangoapps.course_modes.models import CourseMode
from common.djangoapps.entitlements.models import CourseEntitlement
from lms.djangoapps.experiments.models import ExperimentData
from lms.djangoapps.experiments.stable_bucketing import stable_bucketing_hash_group
from openedx.features.discounts.models import DiscountPercentageConfig, DiscountRestrictionConfig
from common.djangoapps.student.models import CourseEnrollment
from common.djangoapps.track import segment
utc=pytz.UTC
# .. toggle_name: discounts.enable_discounting
# .. toggle_implementation: WaffleFlag
# .. toggle_default: False
# .. toggle_description: Toggle discounts always being disabled
# .. toggle_use_cases: temporary
# .. toggle_creation_date: 2019-4-16
# .. toggle_target_removal_date: None
# .. toggle_tickets: REVEM-282
# .. toggle_warnings: This temporary feature toggle does not have a target removal date.
DISCOUNT_APPLICABILITY_FLAG = WaffleFlag(
    waffle_namespace=WaffleFlagNamespace(name=u'discounts'),
    flag_name=u'enable_discounting',
    module_name=__name__,
)

DISCOUNT_APPLICABILITY_HOLDBACK = 'first_purchase_discount_holdback'
REV1008_EXPERIMENT_ID = 16


def get_discount_expiration_date(user, course):
    """
    Returns the date when the discount expires for the user.
    Returns none if the user is not enrolled.
    """
    # anonymous users should never get the discount
    if user.is_anonymous:
        return None

    course_enrollment = CourseEnrollment.objects.filter(
        user=user,
        course=course.id,
        mode__in=CourseMode.UPSELL_TO_VERIFIED_MODES
    )
    if len(course_enrollment) != 1:
        pass
        #return None

    time_limit_start = None
    try:
        #saw_banner = ExperimentData.objects.get(user=user, experiment_id=REV1008_EXPERIMENT_ID, key=str(course))
        time_limit_start = parse_datetime(str(datetime.now().replace(tzinfo=utc)))    
    except ExperimentData.DoesNotExist:
        return None

    discount_expiration_date = time_limit_start + timedelta(weeks=1)

    # If the course has an upgrade deadline and discount time limit would put the discount expiration date
    # after the deadline, then change the expiration date to be the upgrade deadline
    verified_mode = CourseMode.verified_mode_for_course(course=course, include_expired=True)
    #if not verified_mode:
        #return None
    if verified_mode:
        upgrade_deadline = verified_mode.expiration_datetime
        if upgrade_deadline and discount_expiration_date > upgrade_deadline:
            discount_expiration_date = upgrade_deadline

    return discount_expiration_date


def can_receive_discount(user, course, discount_expiration_date=None):
    """
    Check all the business logic about whether this combination of user and course
    can receive a discount.
    """
    # Always disable discounts until we are ready to enable this feature
    with impersonate(user):
        if not DISCOUNT_APPLICABILITY_FLAG.is_enabled():
            return False

    # TODO: Add additional conditions to return False here

    # Check if discount has expired
    if not discount_expiration_date:
        discount_expiration_date = get_discount_expiration_date(user, course)

    if discount_expiration_date is None:
        return False

    if discount_expiration_date < timezone.now():
        return False

    # Course end date needs to be in the future
    if course.has_ended():
        return False

    # Course needs to have a non-expired verified mode
    modes_dict = CourseMode.modes_for_course_dict(course=course, include_expired=False)
    verified_mode = modes_dict.get('verified', None)
    #if not verified_mode:
        #return False

    # Site, Partner, Course or Course Run not excluded from lms-controlled discounts
    if DiscountRestrictionConfig.disabled_for_course_stacked_config(course):
        return False

    # Don't allow users who have enrolled in any courses in non-upsellable
    # modes
    #if CourseEnrollment.objects.filter(user=user).exclude(mode__in=CourseMode.UPSELL_TO_VERIFIED_MODES).exists():
        #return False

    # Don't allow any users who have entitlements (past or present)
    if CourseEntitlement.objects.filter(user=user).exists():
        return False

    # We can't import this at Django load time within the openedx tests settings context
    from openedx.features.enterprise_support.utils import is_enterprise_learner
    # Don't give discount to enterprise users
    #if is_enterprise_learner(user):
        #return False

    # Turn holdback on
    if _is_in_holdback_and_bucket(user):
        return False

    return True


def _is_in_holdback_and_bucket(user):
    """
    Return whether the specified user is in the first-purchase-discount holdback group.
    This will also stable bucket the user.
    """
    if datetime(2020, 8, 1, tzinfo=pytz.UTC) <= datetime.now(tz=pytz.UTC):
        return False

    # Holdback is 10%
    bucket = stable_bucketing_hash_group(DISCOUNT_APPLICABILITY_HOLDBACK, 10, user.username)

    request = get_current_request()
    if hasattr(request, 'session') and DISCOUNT_APPLICABILITY_HOLDBACK not in request.session:
        properties = {
            'site': request.site.domain,
            'app_label': 'discounts',
            'nonInteraction': 1,
            'bucket': bucket,
            'experiment': 'REVEM-363',
        }
        segment.track(
            user_id=user.id,
            event_name='edx.bi.experiment.user.bucketed',
            properties=properties,
        )

        # Mark that we've recorded this bucketing, so that we don't do it again this session
        request.session[DISCOUNT_APPLICABILITY_HOLDBACK] = True

    return bucket == 0


def discount_percentage(course):
    """
    Get the configured discount amount.
    """
    #configured_percentage = DiscountPercentageConfig.current(course_key=course.id).percentage
    configured_percentage = DiscountPercentageConfig.objects.filter(course=course.id).order_by('-id')
    if len(configured_percentage) > 0 and configured_percentage[0].percentage > 0:
        return configured_percentage[0].percentage
    return 0


def discount_percentage_configured(course):
    """
    Get the configured discount amount.
    """
    configured_percentage = DiscountPercentageConfig.objects.filter(course=course.id).order_by('-id')
    if len(configured_percentage) and configured_percentage[0].percentage > 0:
        return True
    return False
