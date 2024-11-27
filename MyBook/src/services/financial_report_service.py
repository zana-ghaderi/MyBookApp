import json
import uuid
from datetime import datetime
from fastapi import HTTPException
from Intuit.MyBook.src.database.cassandra import get_cassandra_session
from Intuit.MyBook.src.kafka.kafka_producer import get_kafka_producer, produce_kafka_message
from Intuit.MyBook.src.models.financial_report import FinancialReport

async def create_financial_report(report: FinancialReport):
    session = get_cassandra_session()
    try:
        # Create report in Cassandra
        report_id = uuid.uuid4()
        session.execute(
            """
            INSERT INTO financial_reports (id, company_id, report_type, data, created_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (report_id, report.company_id, report.report_type, json.dumps(report.data), datetime.now())
        )

        # Publish event to Kafka
        kafka_producer = get_kafka_producer()
        produce_kafka_message(
            kafka_producer,
            'financial-reports-topic',
            str(report_id),  # Use report_id as the key
            {
                'id': str(report_id),
                'company_id': report.company_id,
                'report_type': report.report_type,
                'data': report.data,
                'created_at': datetime.now().isoformat()
            }
        )

        return {"message": "Financial report created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def get_financial_reports(company_id: int):
    session = get_cassandra_session()
    try:
        result = session.execute(
            "SELECT * FROM financial_reports WHERE company_id = %s ALLOW FILTERING",
            (company_id,)
        )
        reports = [{
            "id": str(row.id),
            "company_id": row.company_id,
            "report_type": row.report_type,
            "data": json.loads(row.data),
            "created_at": row.created_at.isoformat()
        } for row in result]
        return reports
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
