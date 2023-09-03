# 使用docker镜像配置飞书告警

```shell
docker run -d -p 1111:8000 -e FEISHU_WEBHOOK_URL='' aweihooo/feishu_notify:1.0
```

# 配置alertmanager 告警

```yaml
- name: 'web.hook'
  webhook_configs:
  - url: 'http://IP:1111/webhook'
```
