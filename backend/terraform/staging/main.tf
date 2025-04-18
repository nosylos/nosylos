resource "aws_elastic_beanstalk_application" "staging-backend" {
  name = var.application
}

resource "aws_elastic_beanstalk_environment" "backend" {
  name                = var.environment
  application         = aws_elastic_beanstalk_application.staging-backend.name
  solution_stack_name = var.solution_stack_name

  # Environment, ELB, EC2
  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "SingleInstance"
  }

  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "InstanceType"
    value     = "t3.micro"
  }

  # Environment variables
  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "ENVIRONMENT"
    value     = "staging"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "STAGING_MASTER_USER_PASS"
    value     = var.STAGING_MASTER_USER_PASS
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "DJANGO_STAGING_SECRET"
    value     = var.DJANGO_STAGING_SECRET
  }

  # Security groups
  setting {
    namespace = "aws:autoscaling:launchconfiguration"
    name      = "SecurityGroups"
    value     = aws_security_group.staging_sg.id
  }

  # DB
  setting {
    namespace = "aws:rds:dbinstance"
    name      = "DBAllocatedStorage"
    value     = "10"
  }

  setting {
    namespace = "aws:rds:dbinstance"
    name      = "DBDeletionPolicy"
    value     = "Delete"
  }

  setting {
    namespace = "aws:rds:dbinstance"
    name      = "HasCoupledDatabase"
    value     = "true"
  }

  setting {
    namespace = "aws:rds:dbinstance"
    name      = "DBEngine"
    value     = "postgres"
  }

  setting {
    namespace = "aws:rds:dbinstance"
    name      = "DBEngineVersion"
    value     = "16.3"
  }

  setting {
    namespace = "aws:rds:dbinstance"
    name      = "DBInstanceClass"
    value     = "db.t3.micro"
  }

  setting {
    namespace = "aws:rds:dbinstance"
    name      = "DBPassword"
    value     = var.POSTGRES_PASSWORD
  }

  setting {
    namespace = "aws:rds:dbinstance"
    name      = "DBUser"
    value     = "postgres"
  }
}
