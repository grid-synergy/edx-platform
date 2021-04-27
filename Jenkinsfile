// ----------------------------------------------------------------------------
// written by:  Lawrence McDaniel
//              lpm0073@gmail.com
//              https://lawrencemcdaniel.com
//
// usage:       Base Jenkins pipeline script to build, test, 
//              merge to koa.master.
//
//              Jenkins host: https://jenkins.gsedxlms.com/
//
//              Jenkins variables: https://jenkins.gsedxlms.com/env-vars.html/
// webhook test #7
// ----------------------------------------------------------------------------
def gv 

pipeline {

    agent { docker { image 'python:3.5.1' } }
    //agent any 

    stages {

        stage("init") {

            steps {
                script {
                    gv = load "Jenkins.pipeline.groovy"
                    gv.initEnvironment()

                    def email_subject = "Jenkins build ${BUILD_ID}: ${GIT_BRANCH} in ${GIT_URL}"
                    def email_body = gv.getGitHubMetadata()
                    def email_providers = [ [$class: 'CulpritsRecipientProvider'], [$class: 'DevelopersRecipientProvider'] ];

                    email_providers.add ( [$class: 'RequesterRecipientProvider'] );

                    emailext (
                        to: 'andrew@gridsynergy.com.sg',
                        recipientProviders: email_providers,
                        subject: email_subject,
                        attachLog: true,
                        body: email_body
                    )
                }
            }

        }

        stage('build') {

            steps {
                script {
                    if (gv.isGSBranch()) {
                        echo 'this is a gs/ branch: building'
                    } else {
                        echo 'this is not a gs/ branch but we will build it anyway'
                    }
                    gv.buildApp()
                }
            }

        }

        stage("test") {

            steps {
                script {
                    if (gv.isGSBranch()) {
                        echo 'this is a gs/ branch: testing'
                    } else {
                        echo 'this is not a gs/ branch but we will test anyway'
                    }
                    gv.testApp()
                }
            }

        }

        stage("deploy") {

            steps {

                script {
                    if (gv.isGSBranch()) {
                        gv.deployApp()
                    } else {
                        echo 'this is not a gs/ branch. not deploying'
                    }
                }

                // requires plugins: Credentials, Credentials Binding
                //withCredentials([
                //    usernamePassword(
                //        credentials: 'gs-edx-staging', 
                //        usernameVariable: USER, 
                //        passwordVariable: PWD)
                //]) {
                //        // user, pwd available here.
                //        echo "username is ${USER}."
                //}
            }

        }        

    }

    // +++++++++++++++++++++++++++++++++++++++++++++++++++++++
    // THESE ARE ACTIONS THAT WE TAKE BASED ON THE JENKINS 
    // PIPELINE RESULT.
    // +++++++++++++++++++++++++++++++++++++++++++++++++++++++
   post {

        always {

            echo 'Cleaning up Jenkins environment...'

        }

        failure {
            
            echo 'Jenkins post - Failure...'
            slackSend channel: '#general', color: 'bad', message: '$DEFAULT_CONTENT'

            script {

                emailext subject: '$DEFAULT_SUBJECT',
                    body: '$DEFAULT_CONTENT',
                    recipientProviders: [
                        [$class: 'DevelopersRecipientProvider'],
                        [$class: 'RequesterRecipientProvider']
                    ], 
                    replyTo: '$DEFAULT_REPLYTO',
                    to: '$DEFAULT_RECIPIENTS'

            }
        }

        success {
            echo 'Jenkins post - Success...'
            echo "This pull request / commit merged into koa.master"
            slackSend channel: '#general', color: 'good', message: '$DEFAULT_CONTENT'

        }

        changed {
            script {
                if (currentBuild.currentResult == 'SUCCESS') { // Other values: SUCCESS, UNSTABLE
                    // Send an email only if the build status has changed from green/unstable to red
                    emailext subject: '$DEFAULT_SUBJECT',
                        body: '$DEFAULT_CONTENT',
                        recipientProviders: [
                            [$class: 'CulpritsRecipientProvider'],
                            [$class: 'DevelopersRecipientProvider'],
                            [$class: 'RequesterRecipientProvider']
                        ], 
                        replyTo: '$DEFAULT_REPLYTO',
                        to: 'andrew@gridsynergy.com.sg'
                    
                    slackSend channel: '#general', color: 'good', message: "The pipeline ${currentBuild.fullDisplayName} ${BRANCH_NAME} has stabilized."

                }

                if (currentBuild.currentResult == 'FAILURE') { // Other values: SUCCESS, UNSTABLE
                    // Send an email only if the build status has changed from green/unstable to red
                    emailext subject: '$DEFAULT_SUBJECT',
                        body: '$DEFAULT_CONTENT',
                        recipientProviders: [[$class: 'CulpritsRecipientProvider']], 
                        replyTo: '$DEFAULT_REPLYTO',
                        to: 'andrew@gridsynergy.com.sg'

                    slackSend channel: '#general', color: 'bad', message: "The pipeline ${currentBuild.fullDisplayName} ${BRANCH_NAME} failed."

                }

                if (currentBuild.currentResult == 'UNSTABLE') { // Other values: SUCCESS, UNSTABLE
                    // Send an email only if the build status has changed from green/unstable to red
                    emailext subject: '$DEFAULT_SUBJECT',
                        body: '$DEFAULT_CONTENT',
                        recipientProviders: [
                            [$class: 'CulpritsRecipientProvider'],
                            [$class: 'DevelopersRecipientProvider'],
                            [$class: 'RequesterRecipientProvider']
                        ], 
                        replyTo: '$DEFAULT_REPLYTO',
                        to: 'andrew@gridsynergy.com.sg'

                    slackSend channel: '#general', color: 'bad', message: "The pipeline ${currentBuild.fullDisplayName} ${BRANCH_NAME} is unstable."

                }

            }
        }


    }    

}