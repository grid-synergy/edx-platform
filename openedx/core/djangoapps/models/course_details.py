"""
CourseDetails
"""


import logging
import re

import six
from django.conf import settings
from openedx.core.djangoapps.models.config.waffle import enable_course_detail_update_certificate_date
from openedx.core.djangoapps.signals.signals import COURSE_CERT_DATE_CHANGE
from openedx.core.djangolib.markup import HTML
from openedx.core.lib.courses import course_image_url
from xmodule.fields import Date
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.exceptions import ItemNotFoundError
from django.apps import apps
import logging
log = logging.getLogger(__name__)


# This list represents the attribute keys for a course's 'about' info.
# Note: The 'video' attribute is intentionally excluded as it must be
# handled separately; its value maps to an alternate key name.
ABOUT_ATTRIBUTES = [
    'syllabus',
    'title',
    'subtitle',
    'duration',
    'description',
    'short_description',
    'overview',
    'effort',
    'entrance_exam_enabled',
    'entrance_exam_id',
    'entrance_exam_minimum_score_pct',
    'about_sidebar_html',
    'allow_review',
]


class CourseDetails(object):
    """
    An interface for extracting course information from the modulestore.
    """
    def __init__(self, org, course_id, run):
        # still need these for now b/c the client's screen shows these 3
        # fields
        self.org = org
        self.course_id = course_id
        self.run = run
        self.language = None
        self.region = None
        self.difficulty_level = None
        self.course_org = None
        self.new_category = None
        self.subcategory = None
        self.platform_visibility = None
        self.premium = None
        self.course_sale_type = None
        self.course_price = None
        self.indexed_in_discovery = None
        self.published_in_ecommerce = None
        self.start_date = None  # 'start'
        self.end_date = None  # 'end'
        self.enrollment_start = None
        self.enrollment_end = None
        self.syllabus = None  # a pdf file asset
        self.title = ""
        self.subtitle = ""
        self.duration = ""
        self.description = ""
        self.short_description = ""
        self.overview = ""  # html to render as the overview
        self.about_sidebar_html = ""
        self.intro_video = None  # a video pointer
        self.effort = None  # hours/week
        self.license = "all-rights-reserved"  # default course license is all rights reserved
        self.course_image_name = ""
        self.course_image_asset_path = ""  # URL of the course image
        self.banner_image_name = ""
        self.banner_image_asset_path = ""
        self.video_thumbnail_image_name = ""
        self.video_thumbnail_image_asset_path = ""
        self.pre_requisite_courses = []  # pre-requisite courses
        self.entrance_exam_enabled = ""  # is entrance exam enabled
        self.entrance_exam_id = ""  # the content location for the entrance exam
        self.entrance_exam_minimum_score_pct = settings.FEATURES.get(
            'ENTRANCE_EXAM_MIN_SCORE_PCT',
            '50'
        )  # minimum passing score for entrance exam content module/tree,
        self.self_paced = None
        self.learning_info = []
        self.instructor_info = []
        self.allow_review = "true"

    @classmethod
    def fetch_about_attribute(cls, course_key, attribute):
        """
        Retrieve an attribute from a course's "about" info
        """
        if attribute not in ABOUT_ATTRIBUTES + ['video']:
            raise ValueError(u"'{0}' is not a valid course about attribute.".format(attribute))

        usage_key = course_key.make_usage_key('about', attribute)
        try:
            value = modulestore().get_item(usage_key).data
        except ItemNotFoundError:
            value = None
        return value

    @classmethod
    def fetch(cls, course_key):
        """
        Fetch the course details for the given course from persistence
        and return a CourseDetails model.
        """
        return cls.populate(modulestore().get_course(course_key))

    @classmethod
    def populate(cls, course_descriptor):
        """
        Returns a fully populated CourseDetails model given the course descriptor
        """
        course_key = course_descriptor.id
        course_details = cls(course_key.org, course_key.course, course_key.run)
        course_details.start_date = course_descriptor.start
        course_details.end_date = course_descriptor.end
        course_details.certificate_available_date = course_descriptor.certificate_available_date
        course_details.enrollment_start = course_descriptor.enrollment_start
        course_details.enrollment_end = course_descriptor.enrollment_end
        course_details.pre_requisite_courses = course_descriptor.pre_requisite_courses
        course_details.course_image_name = course_descriptor.course_image
        course_details.course_image_asset_path = course_image_url(course_descriptor, 'course_image')
        course_details.banner_image_name = course_descriptor.banner_image
        course_details.banner_image_asset_path = course_image_url(course_descriptor, 'banner_image')
        course_details.video_thumbnail_image_name = course_descriptor.video_thumbnail_image
        course_details.video_thumbnail_image_asset_path = course_image_url(course_descriptor, 'video_thumbnail_image')
        course_details.language = course_descriptor.language
        course_details.region = course_descriptor.region
        course_details.difficulty_level = course_descriptor.difficulty_level
        course_details.course_org = course_descriptor.course_org
        course_details.new_category = course_descriptor.new_category
        course_details.subcategory = course_descriptor.subcategory
        course_details.platform_visibility = course_descriptor.platform_visibility
        course_details.premium = course_descriptor.premium
        course_details.course_sale_type = course_descriptor.course_sale_type
        course_details.course_price = course_descriptor.course_price
        CourseOverview = apps.get_model('course_overviews', 'CourseOverview')
        course_details.indexed_in_discovery = CourseOverview.get_from_id(course_key).indexed_in_discovery
        course_details.published_in_ecommerce = CourseOverview.get_from_id(course_key).published_in_ecommerce
        course_details.self_paced = course_descriptor.self_paced
        course_details.learning_info = course_descriptor.learning_info
        course_details.instructor_info = course_descriptor.instructor_info

        # Default course license is "All Rights Reserved"
        course_details.license = getattr(course_descriptor, "license", "all-rights-reserved")

        course_details.intro_video = cls.fetch_youtube_video_id(course_key)

        for attribute in ABOUT_ATTRIBUTES:
            value = cls.fetch_about_attribute(course_key, attribute)
            if value is not None:
                setattr(course_details, attribute, value)

        return course_details

    @classmethod
    def fetch_youtube_video_id(cls, course_key):
        """
        Returns the course about video ID.
        """
        raw_video = cls.fetch_about_attribute(course_key, 'video')
        if raw_video:
            return cls.parse_video_tag(raw_video)

    @classmethod
    def fetch_video_url(cls, course_key):
        """
        Returns the course about video URL.
        """
        video_id = cls.fetch_youtube_video_id(course_key)
        if video_id:
            return "http://www.youtube.com/watch?v={0}".format(video_id)

    @classmethod
    def update_about_item(cls, course, about_key, data, user_id, store=None):
        """
        Update the about item with the new data blob. If data is None,
        then delete the about item.
        """
        temploc = course.id.make_usage_key('about', about_key)
        store = store or modulestore()
        if data is None:
            try:
                store.delete_item(temploc, user_id)
            # Ignore an attempt to delete an item that doesn't exist
            except ValueError:
                pass
        else:
            try:
                about_item = store.get_item(temploc)
            except ItemNotFoundError:
                about_item = store.create_xblock(course.runtime, course.id, 'about', about_key)
            about_item.data = data
            store.update_item(about_item, user_id, allow_not_found=True)

    @classmethod
    def update_about_video(cls, course, video_id, user_id):
        """
        Updates the Course's about video to the given video ID.
        """
        recomposed_video_tag = CourseDetails.recompose_video_tag(video_id)
        cls.update_about_item(course, 'video', recomposed_video_tag, user_id)

    @classmethod
    def update_from_json(cls, course_key, jsondict, user):  # pylint: disable=too-many-statements
        """
        Decode the json into CourseDetails and save any changed attrs to the db
        """
        module_store = modulestore()
        descriptor = module_store.get_course(course_key)

        dirty = False

        # In the descriptor's setter, the date is converted to JSON
        # using Date's to_json method. Calling to_json on something that
        # is already JSON doesn't work. Since reaching directly into the
        # model is nasty, convert the JSON Date to a Python date, which
        # is what the setter expects as input.
        date = Date()

        if 'start_date' in jsondict:
            converted = date.from_json(jsondict['start_date'])
        else:
            converted = None
        if converted != descriptor.start:
            dirty = True
            descriptor.start = converted

        if 'end_date' in jsondict:
            converted = date.from_json(jsondict['end_date'])
        else:
            converted = None

        if converted != descriptor.end:
            dirty = True
            descriptor.end = converted

        if 'enrollment_start' in jsondict:
            converted = date.from_json(jsondict['enrollment_start'])
        else:
            converted = None

        if converted != descriptor.enrollment_start:
            dirty = True
            descriptor.enrollment_start = converted

        if 'enrollment_end' in jsondict:
            converted = date.from_json(jsondict['enrollment_end'])
        else:
            converted = None

        if converted != descriptor.enrollment_end:
            dirty = True
            descriptor.enrollment_end = converted

        if 'certificate_available_date' in jsondict:
            converted = date.from_json(jsondict['certificate_available_date'])
        else:
            converted = None

        if converted != descriptor.certificate_available_date:
            dirty = True
            descriptor.certificate_available_date = converted
            if enable_course_detail_update_certificate_date(course_key):
                COURSE_CERT_DATE_CHANGE.send_robust(sender=cls, course_key=six.text_type(course_key))

        if 'course_image_name' in jsondict and jsondict['course_image_name'] != descriptor.course_image:
            descriptor.course_image = jsondict['course_image_name']
            dirty = True

        if 'banner_image_name' in jsondict and jsondict['banner_image_name'] != descriptor.banner_image:
            descriptor.banner_image = jsondict['banner_image_name']
            dirty = True

        if 'video_thumbnail_image_name' in jsondict \
                and jsondict['video_thumbnail_image_name'] != descriptor.video_thumbnail_image:
            descriptor.video_thumbnail_image = jsondict['video_thumbnail_image_name']
            dirty = True

        if 'pre_requisite_courses' in jsondict \
                and sorted(jsondict['pre_requisite_courses']) != sorted(descriptor.pre_requisite_courses):
            descriptor.pre_requisite_courses = jsondict['pre_requisite_courses']
            dirty = True

        if 'license' in jsondict:
            descriptor.license = jsondict['license']
            dirty = True

        if 'learning_info' in jsondict:
            descriptor.learning_info = jsondict['learning_info']
            dirty = True

        if 'instructor_info' in jsondict:
            descriptor.instructor_info = jsondict['instructor_info']
            dirty = True

        if 'language' in jsondict and jsondict['language'] != descriptor.language:
            descriptor.language = jsondict['language']
            dirty = True

        if 'region' in jsondict and jsondict['region'] != descriptor.region:
            descriptor.region = jsondict['region']
            dirty = True

        if 'difficulty_level' in jsondict and jsondict['difficulty_level'] != descriptor.difficulty_level:
            descriptor.difficulty_level = jsondict['difficulty_level']
            dirty = True

        if 'course_org' in jsondict and jsondict['course_org'] != descriptor.course_org:
            descriptor.course_org = jsondict['course_org']
            dirty = True

        if 'new_category' in jsondict and jsondict['new_category'] != descriptor.new_category:
            descriptor.new_category = jsondict['new_category']
            dirty = True

        if 'subcategory' in jsondict and jsondict['subcategory'] != descriptor.subcategory:
            descriptor.subcategory = jsondict['subcategory']
            dirty = True

        if 'platform_visibility' in jsondict and jsondict['platform_visibility'] != descriptor.platform_visibility:
            descriptor.platform_visibility = jsondict['platform_visibility']
            dirty = True

        if 'premium' in jsondict and jsondict['premium'] != descriptor.premium:
            descriptor.premium = jsondict['premium']
            dirty = True

        if 'course_sale_type' in jsondict and jsondict['course_sale_type'] != descriptor.course_sale_type:
            descriptor.course_sale_type = jsondict['course_sale_type']
            dirty = True


        if 'course_price' in jsondict and jsondict['course_price'] != descriptor.course_price:
            descriptor.course_price = jsondict['course_price']
            dirty = True

        if (descriptor.can_toggle_course_pacing
                and 'self_paced' in jsondict
                and jsondict['self_paced'] != descriptor.self_paced):
            descriptor.self_paced = jsondict['self_paced']
            dirty = True

        if dirty:
            module_store.update_item(descriptor, user.id)

        # NOTE: below auto writes to the db w/o verifying that any of
        # the fields actually changed to make faster, could compare
        # against db or could have client send over a list of which
        # fields changed.
        for attribute in ABOUT_ATTRIBUTES:
            if attribute in jsondict:
                cls.update_about_item(descriptor, attribute, jsondict[attribute], user.id)

        cls.update_about_video(descriptor, jsondict['intro_video'], user.id)

        # Could just return jsondict w/o doing any db reads, but I put
        # the reads in as a means to confirm it persisted correctly
        return CourseDetails.fetch(course_key)

    @staticmethod
    def parse_video_tag(raw_video):
        """
        Because the client really only wants the author to specify the
        youtube key, that's all we send to and get from the client. The
        problem is that the db stores the html markup as well (which, of
        course, makes any site-wide changes to how we do videos next to
        impossible.)
        """
        if not raw_video:
            return None

        keystring_matcher = re.search(r'(?<=embed/)[a-zA-Z0-9_-]+', raw_video)
        if keystring_matcher is None:
            keystring_matcher = re.search(r'<?=\d+:[a-zA-Z0-9_-]+', raw_video)

        if keystring_matcher:
            return keystring_matcher.group(0)
        else:
            logging.warn("ignoring the content because it doesn't not conform to expected pattern: " + raw_video)
            return None

    @staticmethod
    def recompose_video_tag(video_key):
        """
        Returns HTML string to embed the video in an iFrame.
        """
        # TODO should this use a mako template? Of course, my hope is
        # that this is a short-term workaround for the db not storing
        #  the right thing
        result = None
        if video_key:
            result = (
                HTML(u'<iframe title="YouTube Video" width="560" height="315" src="//www.youtube.com/embed/{}?rel=0" '
                     'frameborder="0" allowfullscreen=""></iframe>').format(video_key)
            )
        return result
