# ECS Cluster
resource "aws_ecs_cluster" "cluster" {
  name = "dashboard_cluster"
}

# ECS Task Definition
resource "aws_ecs_task_definition" "task" {
  family                   = "dashboard_task"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "256"  # Adjust as necessary
  memory                   = "512"  # Adjust as necessary

  container_definitions = jsonencode([{
    name      = "dashboard_container"
    image     = "129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12_dashboard_team2:latest"  # Replace with your Docker image URI
    essential = true
    portMappings = [{
      containerPort = 80
      hostPort      = 80
    }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/dashboard"
        "awslogs-region"        = "eu-west-2"  # Adjust as necessary
        "awslogs-stream-prefix" = "ecs"
      }
    }
  }])
}

# ECS Service
resource "aws_ecs_service" "service" {
  name            = "dashboard_service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task.arn
  desired_count   = 1
  launch_type     = "FARGATE"
  network_configuration {
    subnets         = ["subnet-058f02e41ee6a5439", "subnet-0c459ebb007081668","subnet-0ff947058bbc1165d"]  # Replace with your subnet IDs
    security_groups = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}

# Security Group
resource "aws_security_group" "ecs_sg" {
  name        = "ecs_sg"
  description = "Allow HTTP traffic"
  vpc_id      = "vpc-061c17c21b97427d8"  # Replace with your VPC ID

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.cluster.name
}

output "ecs_service_name" {
  value = aws_ecs_service.service.name
}
