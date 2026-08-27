output "rds_endpoint" {
  value = aws_db_instance.postgres.address
}

output "redis_endpoint" {
  value = aws_elasticache_replication_group.redis.primary_endpoint_address
}

output "alb_dns_name" {
  value = aws_lb.app.dns_name
}

output "ec2_instance_ids" {
  value = aws_instance.app[*].id
}