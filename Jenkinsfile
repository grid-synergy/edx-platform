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

pipeline {

    agent { docker { image 'python:3.5.1' } }

    stages {

        stage("init") {

            steps {
                script {
                    gv = load "Jenkins.pipeline.groovy"
                    gv.initEnvironment()
                }
            }

        }

        stage('build') {

            steps {
                sh 'python --version'
            }

        }
    }
}