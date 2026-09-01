from __future__ import annotations

from datetime import datetime, timezone
from io import BytesIO
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


DISCLAIMER = "This report was generated using synthetic prototype data and does not represent live IMD observations."


class ReportService:
    def build_live_monitor_pdf(self, overview: dict[str, Any], stations: list[dict[str, Any]], anomalies: list[dict[str, Any]]) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=1.2 * cm, leftMargin=1.2 * cm, topMargin=1.2 * cm, bottomMargin=1.2 * cm)
        styles = getSampleStyleSheet()
        story = [
            Paragraph("SKYGUARD AI", styles["Title"]),
            Paragraph("Live Monitoring Report", styles["Heading2"]),
            Paragraph("SIMULATION MODE", styles["Heading3"]),
            Paragraph(f"Generated timestamp: {datetime.now(timezone.utc).isoformat()}", styles["Normal"]),
            Spacer(1, 10),
            Paragraph(DISCLAIMER, styles["Italic"]),
            Spacer(1, 14),
            Paragraph("Network Summary", styles["Heading3"]),
        ]

        summary_data = [
            ["Total stations", overview["total_stations"], "Healthy", overview["healthy_stations"]],
            ["Warning", overview["warning_stations"], "Critical", overview["critical_stations"]],
            ["Active anomalies", overview["active_anomalies"], "Data quality", f"{overview['data_quality']}%"],
        ]
        story.append(self._table(summary_data, header=False))
        story.extend([Spacer(1, 14), Paragraph("Station Table", styles["Heading3"])])

        station_data = [["Station ID", "Region", "Temperature", "Pressure", "Relative Humidity", "Health", "Status"]]
        for station in stations:
            station_data.append([
                station["station_id"],
                station["region"],
                self._fmt(station["temperature"], " C"),
                self._fmt(station["pressure"], " hPa"),
                self._fmt(station["relative_humidity"], "%"),
                f"{station['health_score']}%",
                station["status"],
            ])
        story.append(self._table(station_data))
        story.extend([Spacer(1, 14), Paragraph("Anomaly Table", styles["Heading3"])])

        anomaly_data = [["Station", "Timestamp", "Anomaly Type", "Severity", "Confidence"]]
        for anomaly in anomalies or []:
            anomaly_data.append([
                anomaly["station_id"],
                anomaly["timestamp"],
                anomaly["anomaly_type"],
                anomaly["severity"],
                f"{round(float(anomaly['confidence']) * 100, 1)}%",
            ])
        if len(anomaly_data) == 1:
            anomaly_data.append(["No active anomalies", "-", "-", "-", "-"])
        story.append(self._table(anomaly_data))
        doc.build(story)
        return buffer.getvalue()

    @staticmethod
    def _fmt(value: Any, suffix: str) -> str:
        return "missing" if value is None else f"{value}{suffix}"

    @staticmethod
    def _table(data: list[list[Any]], header: bool = True) -> Table:
        table = Table(data, repeatRows=1 if header else 0)
        style = [
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D1D5DB")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ]
        if header:
            style.extend([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#153226")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ])
        table.setStyle(TableStyle(style))
        return table


report_service = ReportService()
