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
// ----------------------------------------------------------------------------
def gv 

// global variables
// ----------------------------------
CODE_CHANGES = getGitChanges()

pipeline {

    // required, but not of interest to us for now.
    agent any

    // optional environment variables
    environment {
        //NEW_VERSION = '1.0.1'
        //SSH_KEY = credentials('gs-edx-staging')
    }

    // optional jenkins job parameters
    parameters {

        //string(name: 'VERSION', defaultValue: 'xx', description: 'Version number to use with koa.master release.')
        //choice(name: 'VERSION',  choices: ['1', '2', '3'], description: 'Version number to use with koa.master release.')
        //booleanParam(name: 'executeTests', defaultValue: true, description, '')

    }

    // optional remote tools that we could include if we wanted
    tools {
        //maven
        //gradle
        //jdk
    }


    // +++++++++++++++++++++++++++++++++++++++++++++++++++++++
    // THE GRID SYNERGY JENKINS PIPELINE STAGES
    // +++++++++++++++++++++++++++++++++++++++++++++++++++++++
    stages {
        stage("init") {

            steps {
                script {
                    gv = load "Jenkins.pipeline.groovy"
                    gv.initEnvironment()
                }
            }

        }
        stage("build") {
            when {
                expression {
                    gv.isGSBranch()
                }
            }
            steps {

                script {
                    gv.buildApp()
                }

            }

        }
        stage("test") {
            when {
                expression {
                    gv.isGSBranch()
                }
            }
            steps {
                gv.testApp()
            }

        }
        stage("deploy") {
            when {
                expression {
                    gv.isGSBranch()
                }
            }
            steps {
                gv.testApp()

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

            gv.cleanupEnvironment()

        }

        failure {

            gv.postFailure()

        }

        success {

            gv.postSuccess()

        }
    }
}