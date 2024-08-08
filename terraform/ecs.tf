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
    image     = "<your-docker-image>"  # Replace with your Docker image URI
    essential = true
    portMappings = [{
      containerPort = 80
      hostPort      = 80
    }]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/dashboard"
        "awslogs-region"        = "us-west-2"  # Adjust as necessary
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
    subnets         = ["<subnet-1>", "<subnet-2>"]  # Replace with your subnet IDs
    security_groups = [aws_security_group.ecs_sg.id]
    assign_public_ip = true
  }
}

# Security Group
resource "aws_security_group" "ecs_sg" {
  name        = "ecs_sg"
  description = "Allow HTTP traffic"
  vpc_id      = "<your-vpc-id>"  # Replace with your VPC ID

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
