// ----------------------------------------------------------------------------
// written by:  Lawrence McDaniel
//              lpm0073@gmail.com
//              https://lawrencemcdaniel.com
//
// usage:       Base Jenkins pipeline groovy script for build, test, deploy
//              Called by JenkinsFile
//
//              Jenkins host: https://jenkins.gsedxlms.com/
//
//  https://jenkins.gsedxlms.com/job/edx-platform-pipeline/job/gs%252Fkoa.master/pipeline-syntax/html
//  setGitHubPullRequestStatus()
//
// ----------------------------------------------------------------------------


def initEnvironment() {


    echo 'Initializing Jenkins environment...'
    echo "Jenkins Build URL: ${BUILD_URL}"
    echo "Jenkins Job URL: ${JOB_URL}"
    echo ''
    echo "Git repository: ${GIT_URL}"
    echo "Git Branch: ${GIT_BRANCH}"
    if (env.CHANGE_AUTHOR) {echo "Git Pull author: ${CHANGE_AUTHOR}"}
    if (env.CHANGE_ID) {echo "Git Pull request: ${CHANGE_ID}"}
    if (env.CHANGE_TARGET) {echo "Git Pull branch target: ${CHANGE_TARGET}"}
    
    echo "Git Commit: ${GIT_COMMIT}"
    echo "Git Build Number: ${BUILD_NUMBER}"
    echo "Git committer: ${GIT_COMMITTER_NAME} ${GIT_COMMITTER_EMAIL}"
    echo "Git author: ${GIT_AUTHOR_NAME} ${GIT_AUTHOR_EMAIL}"
    echo ''
    echo "Initializing Jenkins for version ${NEW_VERSION}"
    echo 'I harken from Jenkins.pipeline.groovy in the root folder of this git repository'
    echo ''

    echo ''
    echo 'Jenkins environment variables:'
    echo '------------------------------'
    echo "BRANCH_NAME: ${BRANCH_NAME}"
    if (env.CHANGE_ID) {
        echo 'optional Pull request variables'
        echo "CHANGE_ID: ${CHANGE_ID}"
        echo "CHANGE_URL ${CHANGE_URL}"
        echo "CHANGE_TITLE ${CHANGE_TITLE}"
        echo "CHANGE_AUTHOR ${CHANGE_AUTHOR}"
        echo "CHANGE_AUTHOR_DISPLAY_NAME ${CHANGE_AUTHOR_DISPLAY_NAME}"
        echo "CHANGE_AUTHOR_EMAIL ${CHANGE_AUTHOR_EMAIL}"
        echo "CHANGE_TARGET ${CHANGE_TARGET}"
        echo "CHANGE_BRANCH ${CHANGE_BRANCH}"
        echo "CHANGE_FORK ${CHANGE_FORK}"
    }
    echo "TAG_NAME ${TAG_NAME}"
    echo "TAG_TIMESTAMP ${TAG_TIMESTAMP}"
    echo "TAG_UNIXTIME ${TAG_UNIXTIME}"
    echo "TAG_DATE ${TAG_DATE}"
    echo "BUILD_NUMBER ${BUILD_NUMBER}"
    echo "BUILD_ID ${BUILD_ID}"
    echo "BUILD_DISPLAY_NAME ${BUILD_DISPLAY_NAME}"
    echo "JOB_NAME ${JOB_NAME}"
    echo "JOB_BASE_NAME ${JOB_BASE_NAME}"
    echo "BUILD_TAG ${BUILD_TAG}"
    echo "EXECUTOR_NUMBER ${EXECUTOR_NUMBER}"
    echo "NODE_NAME ${NODE_NAME}"
    echo "NODE_LABELS ${NODE_LABELS}"
    echo "WORKSPACE ${WORKSPACE}"
    echo "WORKSPACE_TMP ${WORKSPACE_TMP}"
    echo "JENKINS_HOME ${JENKINS_HOME}"
    echo "JENKINS_URL ${JENKINS_URL}"
    echo "BUILD_URL ${BUILD_URL}"
    echo "JOB_URL ${JOB_URL}"
    echo "GIT_COMMIT ${GIT_COMMIT}"
    echo "GIT_PREVIOUS_COMMIT ${GIT_PREVIOUS_COMMIT}"
    echo "GIT_PREVIOUS_SUCCESSFUL_COMMIT ${GIT_PREVIOUS_SUCCESSFUL_COMMIT}"
    echo "GIT_BRANCH ${GIT_BRANCH}"
    echo "GIT_LOCAL_BRANCH ${GIT_LOCAL_BRANCH}"
    echo "GIT_CHECKOUT_DIR ${GIT_CHECKOUT_DIR}"
    echo "GIT_URL ${GIT_URL}"
    echo "GIT_COMMITTER_NAME ${GIT_COMMITTER_NAME}"
    echo "GIT_AUTHOR_NAME ${GIT_AUTHOR_NAME}"
    echo "GIT_COMMITTER_EMAIL ${GIT_COMMITTER_EMAIL}"
    echo "GIT_AUTHOR_EMAIL ${GIT_AUTHOR_EMAIL}"

}



return this