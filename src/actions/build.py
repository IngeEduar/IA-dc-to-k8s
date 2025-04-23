def build_code(intents, data):
    return """
    apiVersion: batch/v1
    kind: CronJob
    metadata:
      name: etl-analytics-hop
    spec:
      timeZone: 'Etc/UTC'
      schedule: "0 2 * * *"
      suspend: true
      concurrencyPolicy: Forbid
      jobTemplate:
        spec:
          backoffLimit: 0
          ttlSecondsAfterFinished: 129600
          template:
            spec:
          containers:
            - name: etl
              image: radmas/mtx-etl-analytics-hop:latest
              imagePullPolicy: IfNotPresent
              volumeMounts:
                - mountPath: /etl/env-mtx-etl.json.template
                  subPath: env-mtx-etl.json.template
                  name: etl-config
              resources:
                requests:
                  memory: "4Gi"
                  cpu: "2000m"
                limits:
                  memory: "4Gi"
                  cpu: "2000m"
              env:
                - name: HOP_OPTIONS
                  value: "-Xms700m -Xmx1500m -Duser.timezone=UTC"
          restartPolicy: Never
          imagePullSecrets:
            - name: secret-registry
          volumes:
            - name: etl-config
              configMap:
                name: etl-config-cm
    """