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

CODE_CHANGES = getGitChanges()
pipeline {

    agent any

    environment {
        NEW_VERSION = '1.0.1'
        SSH_KEY = credentials('gs-edx-staging')
    }

    parameters {

        //string(name: 'VERSION', defaultValue: 'xx', description: 'Version number to use with koa.master release.')
        //choice(name: 'VERSION',  choices: ['1', '2', '3'], description: 'Version number to use with koa.master release.')
        //booleanParam(name: 'executeTests', defaultValue: true, description, '')

    }

    tools {
        //maven
        //gradle
        //jdk
    }

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

            steps {

                script {
                    gv.buildApp()
                }

            }

        }
        stage("test") {
            when {
                expression {
                    // if we indicated that we want to execute tests, 
                    // and we're not currently on koa.master
                    // and the source code has actually been modified
                    //env.BRANCH_NAME != 'koa.master' && 
                    params.executeTests && 
                    CODE_CHANGES == true
                }
            }
            steps {
                gv.testApp()
            }

        }
        stage("deploy") {

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