from typing import Dict
from flask import Blueprint, jsonify, request, Response
from flask.typing import ResponseReturnValue

from prometheus_client import Histogram, Counter, MetricsHandler, generate_latest, REGISTRY, CONTENT_TYPE_LATEST, Summary
import time

bucket_blueprint = Blueprint("zones", __name__)

data: Dict[str, bytes] = {}

# Metrics definitions for Prometheus
REQUEST_TIME = Summary(
    'request_processing_seconds',
    'Time spent processing request'
)

HTTP_REQUEST_DURATION = Histogram(
    "storage_api_http_request_duration_seconds",
    "A histogram of the Storage API request durations in seconds.",
    ["path","method","statusCode"],
    buckets=(.05, .075, .1, .125, .15, .175, .2, .225, .250, .275)
)

@bucket_blueprint.route("/metrics")
def handler_metrics() -> ResponseReturnValue:
    start = time.time()
    try:
        HTTP_REQUEST_DURATION.labels(path="/metrics",method="GET",statusCode=200).observe(time.time() - start)        
        return generate_latest(REGISTRY), 200, {"Content-Type": CONTENT_TYPE_LATEST}
    except:
        HTTP_REQUEST_DURATION.labels(path="/metrics",method="GET",statusCode=500).observe(time.time() - start)        
        return jsonify({"metrics": "error generating metrics output"}), 500, {"Content-Type": "application/json"}
        raise
    


@bucket_blueprint.route("/buckets/<id>")
@REQUEST_TIME.time()
def get_bucket(id: str) -> ResponseReturnValue:    
    start = time.time()    
    if id in data.keys():
        HTTP_REQUEST_DURATION.labels(path="/bucket",method="GET",statusCode=200).observe(time.time() - start)
        return data.get(id), 200, {"Content-Type": "application/octet-stream"}       
    
    HTTP_REQUEST_DURATION.labels(path="/bucket",method="GET",statusCode=404).observe(time.time() - start)
    return jsonify({"error": "not found"}), 404, {"Content-Type": "application/json"}


@bucket_blueprint.route("/buckets/<id>", methods=["PUT"])
@REQUEST_TIME.time()
def put_bucket(id: str) -> ResponseReturnValue:
    start = time.time()
    data[id] = request.get_data()
    HTTP_REQUEST_DURATION.labels(path="/bucket",method="PUT",statusCode=200).observe(time.time() - start)
    return "", 200


@bucket_blueprint.route("/buckets/<id>", methods=["DELETE"])
@REQUEST_TIME.time()
def delete_bucket(id: str) -> ResponseReturnValue:
    start = time.time()
    if id in data.keys():
        data.pop(id, None)
        HTTP_REQUEST_DURATION.labels(path="/bucket",method="DELETE",statusCode=500).observe(time.time() - start)
        return "", 500

    HTTP_REQUEST_DURATION.labels(path="/bucket",method="DELETE",statusCode=400).observe(time.time() - start)    
    return jsonify({"error": "bad request"}), 400, {"Content-Type": "application/json"}
    
