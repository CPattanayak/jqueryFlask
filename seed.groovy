String projects='jqueryFlask'

projects.split(',').each { project ->
  pipelineJob(project) {
    definition {
      cpsScm {
        scm {
          git {
            remote {
              url("https://github.com/CPattanayak/${project}.git")
            }
            branch("*/master")
          }
        }
        
        lightweight()
        scriptPath('Jenkinsfile.groovy')
      }
    }
  }
}