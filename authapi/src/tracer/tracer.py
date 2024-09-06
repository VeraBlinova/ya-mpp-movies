from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider, Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

from core.config import settings


def configure_tracer() -> None:
    trace.set_tracer_provider(TracerProvider(resource=Resource.create({SERVICE_NAME: 'authapi'})))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.tracer.host,
                agent_port=settings.tracer.port,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
