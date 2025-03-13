# ELK Stack Installation & Configuration Guide

---

## **🔹 1️⃣ Clean Up Any Existing Containers & Network**

Before starting fresh, remove any existing ELK containers and the network.

```sh
docker stop es01 kib01 logstash
docker rm es01 kib01 logstash
docker network rm elk
```

---

## **🔹 2️⃣ Create a Docker Network**

We’ll use a dedicated network so that Elasticsearch, Logstash, and Kibana can communicate.

```sh
docker network create elk
```

---

## **🔹 3️⃣ Start Elasticsearch**

Run Elasticsearch as a single-node cluster **without security** (for easier setup).

```sh
docker run -d --name es01 --net elk -p 9200:9200 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.17.3
```

✅ **Test if Elasticsearch is running**:

```sh
curl -X GET "http://localhost:9200/_cluster/health?pretty"
```

If Elasticsearch is working, you should see JSON output showing `"status": "green"` or `"status": "yellow"`.

---

## **🔹 4️⃣ Start Kibana**

Run Kibana and connect it to Elasticsearch.

```sh
docker run -d --name kib01 --net elk -p 5601:5601 \
  -e ELASTICSEARCH_HOSTS="http://es01:9200" \
  -e XPACK_ENCRYPTEDSAVEDOBJECTS_ENCRYPTIONKEY="this_is_a_long_random_string_change_it" \
  docker.elastic.co/kibana/kibana:8.17.3
```

✅ **Check if Kibana is running**:

- Open [**http://localhost:5601**](http://localhost:5601) in your browser.

---

## **🔹 5️⃣ Set Up Logstash Configuration**

Create a **Logstash configuration file** (`logstash.yml`).

#### **Save this as **``** (not **``**)**

```plaintext
input {
  file {
    path => "/logs/app.log"
    start_position => "beginning"
    sincedb_path => "/dev/null"
    mode => "tail"
    codec => multiline {
      pattern => "^%{TIMESTAMP_ISO8601}"
      negate => true
      what => "previous"
    }
  }
}

filter {
  grok {
    match => { "message" => "%{TIMESTAMP_ISO8601:timestamp} - %{LOGLEVEL:level} - %{GREEDYDATA:logmessage}" }
  }
}

output {
  elasticsearch {
    hosts => ["http://es01:9200"]
    index => "logs-%{+YYYY.MM.dd}"
  }
}
```

---

## **🔹 6️⃣ Start Logstash**

Create a volume to store logs
```sh
docker volume create logs_data
```

Now, start Logstash using the configuration.

```sh
docker run --rm -it --net elk \
  -e "XPACK_MONITORING_ENABLED=false" \
  -v "$(pwd)/logstash.conf:/usr/share/logstash/pipeline/logstash.conf" \
  -v logs_data:/logs \
  docker.elastic.co/logstash/logstash:8.17.3
```

✅ **Check if Logstash is running**:

```sh
docker logs -f logstash
```

---

## **🔹 7️⃣ Generate Logs Using Python**

Create and save the following Python script as ``:

```python
import logging
import time

# Configure logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Generate logs
if __name__ == "__main__":
    for i in range(10):
        logging.info(f"Hello World Log {i}")
        time.sleep(1)
    
    logging.error("This is an error message")
```

Run the script:

```sh
docker build -t my-script .
docker run --rm -it -v logs_data:/logs my-script
```

✅ **Check if logs are flowing into Elasticsearch**:

```sh
curl -X GET "http://localhost:9200/_cat/indices?v"
```

You should see an index like:

```
yellow open logs-2024.03.12 xyz123 1 1 100 0 123kb 123kb
```

---

## **🔹 8️⃣ Create Index Pattern in Kibana**

1. Open [**http://localhost:5601**](http://localhost:5601).
2. Click **"Stack Management"** (⚙️ in the left menu).
3. Under **"Kibana"**, go to **"Data Views"** (formerly "Index Patterns").
4. Click **"Create Data View"**.
5. Enter:
   ```
   logs*
   ```
6. Select `` as the time field.
7. Click **"Create Data View"**.

---

## **🔹 9️⃣ View Logs in Kibana**

1. Go to **"Discover"** in Kibana.
2. Select *"logs**"*\* from the dropdown.
3. 🎉 You should now see your logs appearing!

---

## **✅ Summary**

You now have a full **logging pipeline**:

1. **Python script** writes logs (`script.py`).
2. **Logstash** collects logs and sends them to **Elasticsearch**.
3. **Elasticsearch** stores the logs.
4. **Kibana** visualizes the logs.


