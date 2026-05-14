from __future__ import annotations

from flask import Flask, abort, render_template_string, url_for

from app import create_app as create_mfgforge_app
from app import get_db, page
from mfgforge_intelligence import (
    build_interaction_signals,
    build_workflow_definitions,
    summarize_workflow_coverage,
    workflow_by_key,
)


def badge_class(severity: str) -> str:
    if severity in {'critical', 'high'}:
        return 'bad'
    if severity == 'watch':
        return 'warn'
    return 'good'


def create_superforge_app(test_config: dict | None = None) -> Flask:
    app = create_mfgforge_app(test_config)
    register_superforge_routes(app)
    return app


def register_superforge_routes(app: Flask) -> None:
    def superforge_company_pulse() -> str:
        signals = build_interaction_signals(get_db())
        workflows = build_workflow_definitions()
        coverage = summarize_workflow_coverage(workflows)
        active_score = min(100, sum(signal.score for signal in signals) // max(1, len(signals)))
        if active_score >= 70:
            status = 'Critical operational pressure'
            badge = 'bad'
        elif active_score >= 35:
            status = 'Watch closely'
            badge = 'warn'
        else:
            status = 'Stable with normal controls'
            badge = 'good'
        body = render_template_string(
            """
            <section class='page-head'>
                <div>
                    <p class='eyebrow'>SuperForge Intelligence</p>
                    <h2>Company Pulse</h2>
                    <p>Cross-module manufacturing intelligence that reads supplier lead time, machine capacity, material certs, BOM review, quality load, FPY, planning, purchasing, and morale signals without inventing fake business data.</p>
                </div>
                <span class='badge {{ badge }}'>{{ status }}</span>
            </section>
            <section class='panel'>
                <h3>Compiled intelligence score</h3>
                <p><span class='score'>{{ active_score }}</span> / 100</p>
                <p>This score is intentionally lightweight. It surfaces risk and workflow pressure without turning the app into a slow analytics monster.</p>
                <p><a class='button' href='{{ url_for('superforge_intelligence') }}'>Open Intelligence Hub</a></p>
            </section>
            <section class='signals'>
                {% for signal in signals %}
                <article class='signal'>
                    <span class='badge {{ badge_class(signal.severity) }}'>{{ signal.severity }}</span>
                    <strong>{{ signal.title }}</strong>
                    <p><span class='score'>{{ signal.score }}</span> risk score</p>
                    <p>{{ signal.summary }}</p>
                    <p>{{ signal.recommendation }}</p>
                    {% if signal.workflow_key %}<p><a class='button' href='{{ url_for('workflow_detail', workflow_key=signal.workflow_key) }}'>Open Workflow</a></p>{% endif %}
                </article>
                {% endfor %}
            </section>
            <section class='panel'>
                <h3>Workflow coverage</h3>
                <p>{{ workflows|length }} workflow engines cover {{ coverage|length }} source or target tables.</p>
            </section>
            """,
            signals=signals,
            workflows=workflows,
            coverage=coverage,
            active_score=active_score,
            status=status,
            badge=badge,
            badge_class=badge_class,
        )
        return page('Company Pulse | SuperForge', body)

    app.view_functions['company_pulse'] = superforge_company_pulse

    @app.get('/intelligence')
    def superforge_intelligence() -> str:
        signals = build_interaction_signals(get_db())
        workflows = build_workflow_definitions()
        body = render_template_string(
            """
            <section class='page-head'>
                <div>
                    <p class='eyebrow'>Intelligence Hub</p>
                    <h2>Logic between the modules</h2>
                    <p>SuperForge does not just store records. It connects the records into plain-English manufacturing signals and review workflows.</p>
                </div>
            </section>
            <section class='signals'>
                {% for signal in signals %}
                <article class='signal'>
                    <span class='badge {{ badge_class(signal.severity) }}'>{{ signal.severity }}</span>
                    <strong>{{ signal.area }}</strong>
                    <h3>{{ signal.title }}</h3>
                    <p>{{ signal.summary }}</p>
                    <p>{{ signal.recommendation }}</p>
                    <p><small>Sources: {{ signal.source_tables|join(', ') }}</small></p>
                    {% if signal.workflow_key %}<p><a class='button' href='{{ url_for('workflow_detail', workflow_key=signal.workflow_key) }}'>Open linked workflow</a></p>{% endif %}
                </article>
                {% endfor %}
            </section>
            <section class='panel'>
                <h3>Available workflows</h3>
                <table>
                    <thead><tr><th>Workflow</th><th>Area</th><th>Purpose</th></tr></thead>
                    <tbody>
                    {% for workflow in workflows %}
                    <tr>
                        <td><a class='button' href='{{ url_for('workflow_detail', workflow_key=workflow.key) }}'>{{ workflow.title }}</a></td>
                        <td>{{ workflow.area }}</td>
                        <td>{{ workflow.purpose }}</td>
                    </tr>
                    {% endfor %}
                    </tbody>
                </table>
            </section>
            """,
            signals=signals,
            workflows=workflows,
            badge_class=badge_class,
        )
        return page('Intelligence Hub | SuperForge', body)

    @app.get('/workflows/<workflow_key>')
    def workflow_detail(workflow_key: str) -> str:
        workflow = workflow_by_key(workflow_key)
        if workflow is None:
            abort(404)
        body = render_template_string(
            """
            <section class='page-head'>
                <div>
                    <p class='eyebrow'>{{ workflow.area }} Workflow</p>
                    <h2>{{ workflow.title }}</h2>
                    <p>{{ workflow.purpose }}</p>
                </div>
                <a class='button' href='{{ url_for('superforge_intelligence') }}'>Back to Intelligence</a>
            </section>
            <section class='policy'>
                <article class='panel'><h3>Trigger</h3><p>{{ workflow.trigger }}</p></article>
                <article class='panel'><h3>Required review</h3><p>{{ workflow.required_review }}</p></article>
                <article class='panel'><h3>Output</h3><p>{{ workflow.output }}</p></article>
            </section>
            <section class='panel'>
                <h3>Workflow steps</h3>
                <ol>
                {% for step in workflow.steps %}<li>{{ step }}</li>{% endfor %}
                </ol>
            </section>
            <section class='policy'>
                <article class='panel'><h3>Source tables</h3><p>{{ workflow.source_tables|join(', ') }}</p></article>
                <article class='panel'><h3>Target tables</h3><p>{{ workflow.target_tables|join(', ') }}</p></article>
            </section>
            """,
            workflow=workflow,
        )
        return page(f'{workflow.title} | SuperForge', body)
