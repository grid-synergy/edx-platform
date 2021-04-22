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

// returns a list of changed files
// see: https://stackoverflow.com/questions/54175878/which-jenkins-command-to-get-the-list-of-changed-files
@NonCPS
String getChangedFilesList() {

    changedFiles = []
    for (changeLogSet in currentBuild.changeSets) { 
        for (entry in changeLogSet.getItems()) { // for each commit in the detected changes
            for (file in entry.getAffectedFiles()) {
                changedFiles.add(file.getPath()) // add changed file to list
            }
        }
    }

    return changedFiles

}

// true if the branch name begins with "gs/" and there are code modifications.
def isGSBranch() {

    return env.BRANCH_NAME ==~ /gs\/[0-9]+\.[0-9]+\.[0-9]+/ && CODE_CHANGES == true

}

def initEnvironment() {

    changedFiles = getChangedFilesList()

    echo 'Initializing Jenkins environment...'
    echo "Jenkins Build URL: ${BUILD_URL}"
    echo "Jenkins Job URL: ${JOB_URL}"
    echo ''
    echo "Git repository: ${GIT_URL}"
    echo "Git Branch: ${GIT_BRANCH}"
    echo "Git Pull author: ${CHANGE_AUTHOR}"
    echo "Git Pull request: ${CHANGE_ID}"
    echo "Git Pull branch target: ${CHANGE_TARGET}"
    echo "Git Commit: ${GIT_COMMIT}"
    echo "Git Build Number: ${BUILD_NUMBER}"
    echo "Git committer: ${GIT_COMMITTER_NAME} ${GIT_COMMITTER_EMAIL}"
    echo "Git author: ${GIT_AUTHOR_NAME} ${GIT_AUTHOR_EMAIL}"
    echo ''
    echo "Initializing Jenkins for version ${NEW_VERSION}"
    echo 'I harken from Jenkins.pipeline.groovy in the root folder of this git repository'
    echo ''
    echo "Git changed files list: ${changedFiles}"

    echo ''
    echo 'Jenkins environment variables:'
    echo '------------------------------'
    echo "BRANCH_NAME: ${BRANCH_NAME}"
    echo "CHANGE_ID: ${CHANGE_ID}"
    echo "CHANGE_URL ${CHANGE_URL}"
    echo "CHANGE_TITLE ${CHANGE_TITLE}"
    echo "CHANGE_AUTHOR ${CHANGE_AUTHOR}"
    echo "CHANGE_AUTHOR_DISPLAY_NAME ${CHANGE_AUTHOR_DISPLAY_NAME}"
    echo "CHANGE_AUTHOR_EMAIL ${CHANGE_AUTHOR_EMAIL}"
    echo "CHANGE_TARGET ${CHANGE_TARGET}"
    echo "CHANGE_BRANCH ${CHANGE_BRANCH}"
    echo "CHANGE_FORK ${CHANGE_FORK}"
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

def buildApp() {


    // see notes in testApp

    echo 'Building edx-platform...'


}

def testApp() {

    echo 'Testing edx-platform...'

    // a couple of choices for this:
    // 1. run tests on a remote EC2 instance, initiated by calling a bash script.
    // 2. run tests on this EC2 instance.

}

def deployApp() {

    echo 'Deploying edx-platform...'
    echo "Using ssh key ${SSH_KEY}"
    echo "Deploying version ${params.VERSION}"

    // nothing else to do here.

}

def cleanupEnvironment() {

    echo 'Cleaning up Jenkins environment...'

}

def postFailure() {

    echo 'Jenkins post - Failure...'

    // post a message back to the pull requests that Jenkins job failed.


}

def postSuccess() {

    echo 'Jenkins post - Success...'
    echo "This pull request / commit will merge into ${CHANGE_TARGET}"

    // This is currently the best way to push a tag (or a branch, etc) from a
    // Pipeline job. It's not ideal - https://issues.jenkins-ci.org/browse/JENKINS-28335
    // is an open JIRA for getting the GitPublisher Jenkins functionality working
    // with Pipeline.

    // credentialsId here is the credentials you have set up in Jenkins for pushing
    // to that repository using username and password.
    withCredentials([usernamePassword(credentialsId: 'cd31dbc2-0825-40d7-ab0d-9bd198538162', passwordVariable: 'GIT_PASSWORD', usernameVariable: 'GIT_USERNAME')]) {
        sh("git tag -a some_tag -m 'Jenkins'")
        sh('git push https://${GIT_USERNAME}:${GIT_PASSWORD}@<REPO> --tags')
    }

    // For SSH private key authentication, try the sshagent step from the SSH Agent plugin.
    //sshagent (credentials: ['git-ssh-credentials-ID']) {
    //    sh("git tag -a some_tag -m 'Jenkins'")
    //    sh('git push <REPO> --tags')
    //
    //}


}

return this