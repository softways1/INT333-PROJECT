output "instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.devops_server.id
}

output "public_ip" {
  description = "EC2 Public IP Address"
  value       = aws_instance.devops_server.public_ip
}

output "public_dns" {
  description = "EC2 Public DNS name"
  value       = aws_instance.devops_server.public_dns
}

output "ssh_command" {
  description = "SSH connection helper command"
  value       = "ssh -i ${var.key_name}.pem ubuntu@${aws_instance.devops_server.public_ip}"
}
