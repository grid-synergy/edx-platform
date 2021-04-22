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
    //echo "Initializing Jenkins for version ${NEW_VERSION}"
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

    if (env.TAG_NAME) {
        echo 'optional Git Tag variables'
        echo "TAG_NAME ${TAG_NAME}"
        echo "TAG_TIMESTAMP ${TAG_TIMESTAMP}"
        echo "TAG_UNIXTIME ${TAG_UNIXTIME}"
        echo "TAG_DATE ${TAG_DATE}"
    }

    
    if (env.BUILD_NUMBER) {echo "BUILD_NUMBER ${BUILD_NUMBER}"}
    if (env.BUILD_ID) {echo "BUILD_ID ${BUILD_ID}"}
    if (env.BUILD_DISPLAY_NAME) {echo "BUILD_DISPLAY_NAME ${BUILD_DISPLAY_NAME}"}
    if (env.BUILD_TAG) {echo "BUILD_TAG ${BUILD_TAG}"}
    if (env.BUILD_URL) {echo "BUILD_URL ${BUILD_URL}"}

    if (env.JOB_NAME) {echo "JOB_NAME ${JOB_NAME}"}
    if (env.JOB_BASE_NAME) {echo "JOB_BASE_NAME ${JOB_BASE_NAME}"}
    if (env.JOB_URL) {echo "JOB_URL ${JOB_URL}"}

    if (env.EXECUTOR_NUMBER) {echo "EXECUTOR_NUMBER ${EXECUTOR_NUMBER}"}
    if (env.NODE_NAME) {echo "NODE_NAME ${NODE_NAME}"}
    if (env.NODE_LABELS) {echo "NODE_LABELS ${NODE_LABELS}"}
    if (env.WORKSPACE) {echo "WORKSPACE ${WORKSPACE}"}
    if (env.WORKSPACE_TMP) {echo "WORKSPACE_TMP ${WORKSPACE_TMP}"}
    if (env.JENKINS_HOME) {echo "JENKINS_HOME ${JENKINS_HOME}"}
    if (env.JENKINS_URL) {echo "JENKINS_URL ${JENKINS_URL}"}

    if (env.GIT_COMMIT) {echo "GIT_COMMIT ${GIT_COMMIT}"}
    if (env.GIT_PREVIOUS_COMMIT) {echo "GIT_PREVIOUS_COMMIT ${GIT_PREVIOUS_COMMIT}"}
    if (env.GIT_PREVIOUS_SUCCESSFUL_COMMIT) {echo "GIT_PREVIOUS_SUCCESSFUL_COMMIT ${GIT_PREVIOUS_SUCCESSFUL_COMMIT}"}
    if (env.GIT_BRANCH) {echo "GIT_BRANCH ${GIT_BRANCH}"}
    if (env.GIT_LOCAL_BRANCH) {echo "GIT_LOCAL_BRANCH ${GIT_LOCAL_BRANCH}"}
    if (env.GIT_CHECKOUT_DIR) {echo "GIT_CHECKOUT_DIR ${GIT_CHECKOUT_DIR}"}
    if (env.GIT_URL) {echo "GIT_URL ${GIT_URL}"}
    if (env.GIT_COMMITTER_NAME) {echo "GIT_COMMITTER_NAME ${GIT_COMMITTER_NAME}"}
    if (env.GIT_AUTHOR_NAME) {echo "GIT_AUTHOR_NAME ${GIT_AUTHOR_NAME}"}
    if (env.GIT_COMMITTER_EMAIL) {echo "GIT_COMMITTER_EMAIL ${GIT_COMMITTER_EMAIL}"}
    if (env.GIT_AUTHOR_EMAIL) {echo "GIT_AUTHOR_EMAIL ${GIT_AUTHOR_EMAIL}"}

}



return this