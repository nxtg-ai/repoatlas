# NEXUS — Atlas (P-15) Vision-to-Execution Dashboard

> **Owner**: Asif Waliuddin
> **Last Updated**: 2026-03-23
> **North Star**: Portfolio Intelligence for AI Engineering Teams
> **ID**: P-15 | **Machine**: NXTG-AI | **Health**: GREEN

---

## Executive Dashboard

| ID | Initiative | Pillar | Status | Priority | Last Touched |
|----|-----------|--------|--------|----------|-------------|
| N-01 | [Tech Stack Detection](#n-01-tech-stack-detection) | DETECTION | SHIPPED | P0 | 2026-03-04 |
| N-02 | [Health Scoring](#n-02-health-scoring) | INTELLIGENCE | SHIPPED | P0 | 2026-03-04 |
| N-03 | [Cross-Project Patterns](#n-03-cross-project-patterns) | INTELLIGENCE | SHIPPED | P0 | 2026-03-04 |
| N-04 | [Terminal Dashboard](#n-04-terminal-dashboard) | EXPERIENCE | SHIPPED | P0 | 2026-03-04 |
| N-05 | [GitHub CI](#n-05-github-ci) | DISTRIBUTION | SHIPPED | P1 | 2026-03-04 |
| N-06 | [PyPI Publishing](#n-06-pypi-publishing) | DISTRIBUTION | SHIPPED | P0 | 2026-03-04 |
| N-07 | [README + GIF Demo](#n-07-readme-gif-demo) | DISTRIBUTION | SHIPPED | P1 | 2026-03-13 |
| N-08 | [Show HN Launch](#n-08-show-hn-launch) | DISTRIBUTION | DECIDED | P1 | 2026-03-13 |
| N-09 | [Pro Tier / Monetization](#n-09-pro-tier-monetization) | DISTRIBUTION | DECIDED | P2 | 2026-03-13 |
| N-10 | [Tag-Based Release Automation](#n-10-tag-based-release-automation) | DISTRIBUTION | SHIPPED | P1 | 2026-03-13 |
| N-11 | [CLI Integration Tests](#n-11-cli-integration-tests) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-12 | [Doctor — Actionable Recommendations](#n-12-doctor-actionable-recommendations) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-13 | [Scan History & Trends](#n-13-scan-history--trends) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-14 | [CI Mode](#n-14-ci-mode) | DISTRIBUTION | SHIPPED | P1 | 2026-03-13 |
| N-15 | [Project Comparison](#n-15-project-comparison) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-16 | [Configuration File](#n-16-configuration-file) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-17 | [Infrastructure Detection](#n-17-infrastructure-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-18 | [Infrastructure Intelligence](#n-18-infrastructure-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-19 | [Security Posture Detection](#n-19-security-posture-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-20 | [Portfolio Summary Panel](#n-20-portfolio-summary-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-21 | [AI/ML Tooling Detection](#n-21-aiml-tooling-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-22 | [Rich Markdown Export](#n-22-rich-markdown-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-23 | [Security Intelligence](#n-23-security-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-24 | [Code Quality Tooling Detection](#n-24-code-quality-tooling-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-25 | [Quality Intelligence](#n-25-quality-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-26 | [Enhanced Doctor Recommendations](#n-26-enhanced-doctor-recommendations) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-27 | [AI/ML Intelligence](#n-27-aiml-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-28 | [Testing Framework Detection](#n-28-testing-framework-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-29 | [Testing Intelligence](#n-29-testing-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-30 | [Testing Summary Panel](#n-30-testing-summary-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-13 |
| N-31 | [Enhanced Database Detection](#n-31-enhanced-database-detection) | DETECTION | SHIPPED | P1 | 2026-03-13 |
| N-32 | [Database Intelligence](#n-32-database-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-13 |
| N-33 | [Database Summary Panel](#n-33-database-summary-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-34 | [Package Manager Detection](#n-34-package-manager-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-35 | [Package Manager Intelligence](#n-35-package-manager-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-36 | [Package Manager Summary Panel](#n-36-package-manager-summary-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-37 | [License Detection](#n-37-license-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-38 | [License Intelligence](#n-38-license-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-39 | [License Summary Panel](#n-39-license-summary-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-40 | [Enhanced JSON Export](#n-40-enhanced-json-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-41 | [Documentation Artifacts Detection](#n-41-documentation-artifacts-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-42 | [Documentation Artifacts Intelligence](#n-42-documentation-artifacts-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-43 | [CI/CD Configuration Detection](#n-43-cicd-configuration-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-44 | [Filterable Project List](#n-44-filterable-project-list) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-45 | [CI/CD Configuration Intelligence](#n-45-cicd-configuration-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-46 | [Dashboard Quick Insights](#n-46-dashboard-quick-insights) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-47 | [Runtime Version Detection](#n-47-runtime-version-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-48 | [Runtime Version Intelligence](#n-48-runtime-version-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-49 | [CSV Export](#n-49-csv-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-50 | [Build & Task Runner Detection](#n-50-build--task-runner-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-51 | [Build Tool Intelligence](#n-51-build-tool-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-52 | [API Specification Detection](#n-52-api-specification-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-53 | [API Specification Intelligence](#n-53-api-specification-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-54 | [Health Trend Sparklines](#n-54-health-trend-sparklines) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-55 | [Monitoring & Observability Detection](#n-55-monitoring--observability-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-56 | [Monitoring & Observability Intelligence](#n-56-monitoring--observability-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-57 | [Markdown Badge Generation](#n-57-markdown-badge-generation) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-58 | [Authentication & Auth Detection](#n-58-authentication--auth-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-59 | [Authentication Intelligence](#n-59-authentication-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-60 | [Connection Category Filtering](#n-60-connection-category-filtering) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-61 | [Messaging & Notification Detection](#n-61-messaging--notification-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-62 | [Messaging & Notification Intelligence](#n-62-messaging--notification-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-63 | [Connection Statistics Panel](#n-63-connection-statistics-panel) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-64 | [Deployment Target Detection](#n-64-deployment-target-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-65 | [Deployment Target Intelligence](#n-65-deployment-target-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-66 | [Export Format Auto-Detection](#n-66-export-format-auto-detection) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-67 | [Frontend State Management Detection](#n-67-frontend-state-management-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-68 | [State Management Intelligence](#n-68-state-management-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-69 | [Doctor Category Summary](#n-69-doctor-category-summary) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-70 | [CSS & Styling Framework Detection](#n-70-css--styling-framework-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-71 | [CSS & Styling Intelligence](#n-71-css--styling-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-72 | [Connection Category List Command](#n-72-connection-category-list-command) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-73 | [Bundler & Module Tool Detection](#n-73-bundler--module-tool-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-74 | [Bundler Intelligence](#n-74-bundler-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-75 | [Export Connection Summary Stats](#n-75-export-connection-summary-stats) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-76 | [ORM & Database Client Detection](#n-76-orm--database-client-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-77 | [ORM Intelligence](#n-77-orm-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-78 | [Connection Severity Filtering](#n-78-connection-severity-filtering) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-79 | [i18n & Localization Detection](#n-79-i18n--localization-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-80 | [i18n Intelligence](#n-80-i18n-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-81 | [Project Search Command](#n-81-project-search-command) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-82 | [Validation & Schema Library Detection](#n-82-validation--schema-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-83 | [Validation Intelligence](#n-83-validation-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-84 | [Batch Remove Stale Projects](#n-84-batch-remove-stale-projects) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-85 | [Logging Framework Detection](#n-85-logging-framework-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-86 | [Logging Intelligence](#n-86-logging-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-87 | [Rename Project Command](#n-87-rename-project-command) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-88 | [Container Orchestration Detection](#n-88-container-orchestration-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-89 | [Container Orchestration Intelligence](#n-89-container-orchestration-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-90 | [Cloud Provider & SDK Detection](#n-90-cloud-provider--sdk-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-91 | [Cloud Provider Intelligence](#n-91-cloud-provider-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-92 | [Top Projects & Version Commands](#n-92-top-projects--version-commands) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-93 | [Task Queue & Background Job Detection](#n-93-task-queue--background-job-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-94 | [Task Queue Intelligence](#n-94-task-queue-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-95 | [Export Filtering](#n-95-export-filtering) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-96 | [Search Engine Detection](#n-96-search-engine-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-97 | [Search Engine Intelligence](#n-97-search-engine-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-98 | [Doctor JSON Export](#n-98-doctor-json-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-99 | [Feature Flag Detection](#n-99-feature-flag-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-100 | [Feature Flag Intelligence](#n-100-feature-flag-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-101 | [Connections JSON Export](#n-101-connections-json-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-102 | [HTTP Client Detection](#n-102-http-client-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-103 | [HTTP Client Intelligence](#n-103-http-client-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-104 | [Connections CSV Export](#n-104-connections-csv-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-105 | [Documentation Generation Detection](#n-105-documentation-generation-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-106 | [Documentation Generation Intelligence](#n-106-documentation-generation-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-107 | [Doctor CSV Export](#n-107-doctor-csv-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-108 | [CLI Framework Detection](#n-108-cli-framework-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-109 | [CLI Framework Intelligence](#n-109-cli-framework-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-110 | [Status JSON Export](#n-110-status-json-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-111 | [Configuration Management Detection](#n-111-configuration-management-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-112 | [Configuration Management Intelligence](#n-112-configuration-management-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-113 | [Compare JSON Export](#n-113-compare-json-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-114 | [Caching Library Detection](#n-114-caching-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-115 | [Caching Intelligence](#n-115-caching-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-116 | [Top Projects JSON Export](#n-116-top-projects-json-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-117 | [Template Engine Detection](#n-117-template-engine-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-118 | [Template Engine Intelligence](#n-118-template-engine-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-119 | [Search JSON Export](#n-119-search-json-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-120 | [Serialization Format Detection](#n-120-serialization-format-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-121 | [Serialization Format Intelligence](#n-121-serialization-format-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-122 | [Doctor Category Filter](#n-122-doctor-category-filter) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-123 | [Dependency Injection Detection](#n-123-dependency-injection-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-124 | [Dependency Injection Intelligence](#n-124-dependency-injection-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-125 | [Connections Project Filter](#n-125-connections-project-filter) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-126 | [WebSocket Library Detection](#n-126-websocket-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-127 | [WebSocket Intelligence](#n-127-websocket-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-128 | [Connections Summary Mode](#n-128-connections-summary-mode) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-129 | [GraphQL Library Detection](#n-129-graphql-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-130 | [Doctor Priority Filter](#n-130-doctor-priority-filter) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-131 | [GraphQL Intelligence](#n-131-graphql-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-132 | [Event Streaming Detection](#n-132-event-streaming-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-133 | [Status Grade Distribution](#n-133-status-grade-distribution) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-134 | [Event Streaming Intelligence](#n-134-event-streaming-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-135 | [Payment & Billing Detection](#n-135-payment--billing-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-136 | [Status CSV Export](#n-136-status-csv-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-137 | [Compare CSV Export](#n-137-compare-csv-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-138 | [Date & Time Library Detection](#n-138-date--time-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-139 | [Payment & Billing Intelligence](#n-139-payment--billing-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-140 | [Top Projects CSV Export](#n-140-top-projects-csv-export) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-141 | [Image Processing Library Detection](#n-141-image-processing-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-142 | [Date & Time Intelligence](#n-142-date--time-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-143 | [Status Sort Command](#n-143-status-sort-command) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-144 | [Image Processing Intelligence](#n-144-image-processing-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-145 | [Cryptography Library Detection](#n-145-cryptography-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-146 | [PDF & Document Library Detection](#n-146-pdf--document-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-147 | [Connections Sort Command](#n-147-connections-sort-command) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-148 | [Data Visualization Library Detection](#n-148-data-visualization-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-149 | [Data Visualization Intelligence](#n-149-data-visualization-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-150 | [Doctor Sort Command](#n-150-doctor-sort-command) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-151 | [Geospatial & Mapping Library Detection](#n-151-geospatial--mapping-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-152 | [Geospatial Intelligence](#n-152-geospatial-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-153 | [Search Sort Command](#n-153-search-sort-command) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-154 | [Audio/Video & Media Library Detection](#n-154-audiovideo--media-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-155 | [Media Intelligence](#n-155-media-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-156 | [Export Sort Command](#n-156-export-sort-command) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-157 | [Math & Scientific Computing Detection](#n-157-math--scientific-computing-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-158 | [Math Intelligence](#n-158-math-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-159 | [Top Projects Filter](#n-159-top-projects-filter) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-160 | [Concurrency & Async Library Detection](#n-160-concurrency--async-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-161 | [Async Intelligence](#n-161-async-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-162 | [Doctor Project Filter](#n-162-doctor-project-filter) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-163 | [Compression & Archive Library Detection](#n-163-compression--archive-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-164 | [Cryptography Intelligence](#n-164-cryptography-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-165 | [Search Result Limit](#n-165-search-result-limit) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-166 | [PDF & Document Intelligence](#n-166-pdf--document-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-167 | [Email & SMTP Library Detection](#n-167-email--smtp-library-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-168 | [Connections Result Limit](#n-168-connections-result-limit) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-169 | [Accessibility & A11y Tool Detection](#n-169-accessibility--a11y-tool-detection) | DETECTION | SHIPPED | P1 | 2026-03-21 |
| N-170 | [Email Intelligence](#n-170-email-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-21 |
| N-171 | [Doctor Result Limit](#n-171-doctor-result-limit) | EXPERIENCE | SHIPPED | P1 | 2026-03-21 |
| N-172 | [Web Scraping & Crawling Detection](#n-172-web-scraping--crawling-detection) | DETECTION | SHIPPED | P1 | 2026-03-22 |
| N-173 | [Compression Intelligence](#n-173-compression-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-174 | [Export Result Limit](#n-174-export-result-limit) | EXPERIENCE | SHIPPED | P1 | 2026-03-22 |
| N-175 | [Desktop & Cross-Platform Framework Detection](#n-175-desktop--cross-platform-framework-detection) | DETECTION | SHIPPED | P1 | 2026-03-22 |
| N-176 | [A11y Intelligence](#n-176-a11y-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-177 | [Status Result Limit](#n-177-status-result-limit) | EXPERIENCE | SHIPPED | P1 | 2026-03-22 |
| N-178 | [Scraping Intelligence](#n-178-scraping-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-179 | [Desktop Framework Intelligence](#n-179-desktop-framework-intelligence) | INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-180 | [File Storage & Object Store Detection + Intelligence](#n-180-file-storage--object-store-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-181 | [Form Library Detection + Intelligence](#n-181-form-library-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-182 | [Animation Library Detection + Intelligence](#n-182-animation-library-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-183 | [Routing Library Detection + Intelligence](#n-183-routing-library-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-184 | [Game Development Framework Detection + Intelligence](#n-184-game-development-framework-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-185 | [CMS & Headless CMS Detection + Intelligence](#n-185-cms--headless-cms-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-186 | [Rate Limiting Detection + Intelligence](#n-186-rate-limiting-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-187 | [Database Migration Detection + Intelligence](#n-187-database-migration-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-188 | [gRPC & RPC Framework Detection + Intelligence](#n-188-grpc--rpc-framework-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-189 | [Code Generation Tool Detection + Intelligence](#n-189-code-generation-tool-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-190 | [Mocking & Test Fixture Detection + Intelligence](#n-190-mocking--test-fixture-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-191 | [Changelog & Release Tool Detection + Intelligence](#n-191-changelog--release-tool-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-192 | [E2E & Browser Testing Detection + Intelligence](#n-192-e2e--browser-testing-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-193 | [Monorepo Tool Detection + Intelligence](#n-193-monorepo-tool-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-194 | [Error Tracking & APM Detection + Intelligence](#n-194-error-tracking--apm-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-195 | [Static Site Generator Detection + Intelligence](#n-195-static-site-generator-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-196 | [Analytics & Product Analytics Detection + Intelligence](#n-196-analytics--product-analytics-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-197 | [Mobile Framework Detection + Intelligence](#n-197-mobile-framework-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-22 |
| N-198 | [Workflow Engine Detection + Intelligence](#n-198-workflow-engine-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-23 |
| N-199 | [Secrets Management Detection + Intelligence](#n-199-secrets-management-detection--intelligence) | DETECTION+INTELLIGENCE | SHIPPED | P1 | 2026-03-23 |

**Summary**: 196/199 SHIPPED | 3 DECIDED | 0 IDEA | 0 BUILDING

---

## Vision Pillars

### DETECTION — "Know what you have"
- Automatic tech stack detection across Python/TS/Rust/Go/Java
- File-level analysis, dependency parsing, framework identification
- Infrastructure & deployment: Docker, K8s, Terraform, cloud providers, serverless
- Security posture: Dependabot, Renovate, Snyk, CodeQL, Bandit, Gitleaks, Trivy, SECURITY.md
- AI/ML tooling: Anthropic, OpenAI, LangChain, LlamaIndex, Transformers, PyTorch, TensorFlow, Vercel AI SDK, MLflow, W&B, DVC, Jupyter
- Code quality tooling: Ruff, Flake8, Pylint, ESLint, Biome, Black, Prettier, mypy, Pyright, TypeScript, golangci-lint, Clippy
- Testing frameworks: pytest, Jest, Vitest, Mocha, Cypress, Playwright, go test, cargo test, tox, nox, Hypothesis, AVA, Testing Library
- Database & data stores: PostgreSQL, MySQL, SQLite, MongoDB, Redis, Elasticsearch, Neo4j, Cassandra, InfluxDB, DynamoDB, Firestore, Supabase, PlanetScale, CockroachDB, ChromaDB, Pinecone, Qdrant, Weaviate, Kafka, RabbitMQ, Memcached
- Package managers & build tools: pip, Poetry, PDM, uv, Pipenv, setuptools, Hatch, Flit, npm, Yarn, pnpm, Bun, Cargo, Go Modules, Bundler, Maven, Gradle, NuGet, Composer
- License detection: MIT, Apache-2.0, GPL-2.0/3.0, AGPL-3.0, LGPL, BSD-2/3, ISC, MPL-2.0, Unlicense, CC0 from LICENSE files and package configs
- Documentation artifacts: README, CHANGELOG, CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, LICENSE, docs/, API specs (OpenAPI/Swagger), .editorconfig
- CI/CD configuration: GitHub Actions workflows (release/deploy detection), GitLab CI, PR templates, issue templates, CODEOWNERS, Dependabot/Renovate config, pre-commit, git hooks (.husky/.githooks), .gitattributes
- Runtime version detection: .python-version, .node-version, .nvmrc, .ruby-version, .java-version, go.mod, rust-toolchain, .tool-versions (asdf), pyproject.toml requires-python, package.json engines
- Build & task runner detection: Make, Taskfile, Just, tox, nox, Invoke, doit, npm scripts, Gradle, Maven, CMake, Meson, Bazel, Rake, Earthly
- API specification detection: OpenAPI/Swagger, GraphQL, gRPC/Protobuf, AsyncAPI, JSON Schema, tRPC, WSDL/SOAP
- Monitoring & observability: Sentry, Datadog, New Relic, OpenTelemetry, Prometheus, Bugsnag, Rollbar, Honeycomb, Loguru, structlog, Winston, Pino, LogRocket, Logtail, tracing (Rust), Elastic APM
- Authentication & authorization: NextAuth.js, Auth.js, Passport.js, Clerk, Auth0, Firebase Auth, Supabase Auth, Lucia, Keycloak, Flask-Login, django-allauth, FastAPI-Users, Authlib, PyJWT, golang-jwt, Casbin
- Messaging & notifications: SendGrid, Twilio, Slack SDK, Nodemailer, Resend, Pusher, Socket.IO, BullMQ, Celery, Novu, Postmark, Firebase Cloud Messaging, Gomail, Lettre
- Deployment targets: Vercel, Netlify, Fly.io, Railway, Render, Heroku, Firebase Hosting, AWS Amplify, Serverless Framework, Google App Engine, DigitalOcean App Platform, Cloudflare Workers, GitHub Pages
- Frontend state management: Redux, Zustand, Recoil, Jotai, Valtio, MobX, XState, Pinia, Vuex, NgRx, Signals, Effector, Nanostores, Legend State
- CSS & styling frameworks: Tailwind CSS, Styled Components, Emotion, Sass, Less, PostCSS, CSS Modules, Vanilla Extract, Linaria, Panda CSS, UnoCSS, Windi CSS, Bootstrap, Bulma, Chakra UI, Mantine, Material UI, Vuetify, Ant Design, Radix UI, shadcn/ui, Stitches, Twin Macro, Stylelint
- Bundlers & module tools: Webpack, Vite, esbuild, Rollup, Parcel, SWC, Turborepo, Rspack, tsup, unbuild, microbundle, Snowpack, WMR, Turbopack, Bun
- ORM & database clients: SQLAlchemy, Django ORM, Peewee, Tortoise ORM, SQLModel, Prisma, TypeORM, Sequelize, Drizzle, Knex, Mongoose, Kysely, MikroORM, GORM, sqlx, ent, Diesel, SeaORM, Hibernate, MyBatis, jOOQ, Spring Data JPA
- i18n & localization: i18next, react-i18next, next-i18next, next-intl, react-intl, FormatJS, vue-i18n, Angular i18n, Lingui, typesafe-i18n, Babel, Flask-Babel, go-i18n, Go x/text, Fluent, rust-i18n, locale directories
- Validation & schema libraries: Pydantic, marshmallow, Cerberus, attrs, cattrs, Voluptuous, schema, jsonschema, Colander, Schematics, Zod, Yup, Joi, class-validator, Ajv, Superstruct, Valibot, io-ts, TypeBox, Vest, ArkType, Effect Schema, go-playground/validator, ozzo-validation, validator (Rust), garde, Hibernate Validator, Jakarta Validation
- Logging frameworks: Loguru, structlog, python-json-logger, coloredlogs, Logbook, Winston, Pino, Bunyan, log4js, Morgan, Consola, tslog, Zap, Logrus, zerolog, slog, tracing (Rust), env_logger, log4rs, Logback, Log4j, SLF4J
- Container orchestration: Docker Compose, Kubernetes, Helm, Kustomize, Skaffold, Tilt, Terraform, Pulumi, Ansible, Nomad, Docker Swarm, Vagrant, Packer
- Cloud provider & SDK detection: AWS (boto3, aws-sdk, aws-cdk), GCP (google-cloud-*, firebase), Azure (azure-*), Cloudflare (wrangler), Fly.io, Railway, Render, DigitalOcean — across Python, JS/TS, Go, Rust, Java
- Task queue & background job detection: Celery, RQ, Dramatiq, Huey, arq, TaskIQ, Temporal, Prefect, Airflow, Luigi, Dagster, BullMQ, Bull, Bee-Queue, Agenda, node-cron, Graphile Worker, pg-boss, Quirrel, Asynq, robfig/cron, gocraft/work, tokio-cron-scheduler, Apalis, Quartz, Spring Batch — across Python, JS/TS, Go, Rust, Java
- Search engine detection: Elasticsearch, OpenSearch, Meilisearch, Typesense, Algolia, Solr, Whoosh, Haystack, Tantivy, Lunr, FlexSearch, Fuse.js, MiniSearch, Bleve, Lucene — across Python, JS/TS, Go, Rust, Java
- Feature flag detection: LaunchDarkly, Unleash, Flagsmith, GrowthBook, Split, PostHog, Statsig, OpenFeature, Waffle, ConfigCat, Vercel Flags, HappyKit, Togglz, FF4J, Flipper — across Python, JS/TS, Go, Rust, Java
- HTTP client detection: Requests, HTTPX, aiohttp, urllib3, httplib2, PycURL, treq, asks, niquests, Uplink (Python), Axios, node-fetch, Got, Ky, SuperAgent, Undici, ofetch, Wretch, Needle, cross-fetch, isomorphic-fetch (JS/TS), Resty, go-retryablehttp, Gentleman, Sling, Heimdall, Req (Go), reqwest, hyper, ureq, surf, isahc, attohttpc (Rust), OkHttp, Apache HttpClient, Retrofit, Unirest, WebClient, RestTemplate, Feign (Java)
- Documentation generation detection: Sphinx, MkDocs, pdoc, pydoctor (Python), Docusaurus, Storybook, VitePress, TypeDoc, JSDoc, Nextra, GitBook, Docsify, Mintlify, Starlight, documentation.js (JS/TS), mdBook (Rust), Javadoc, Dokka (Java), Doxygen, Swag (Go) — via deps, config files, and directory markers
- CLI framework detection: Click, Typer, Fire, Rich, Textual, Cement, cliff, docopt, plac, Cleo, prompt_toolkit, Questionary, InquirerPy, Trogon (Python), Commander.js, Yargs, meow, oclif, Vorpal, Caporal, Inquirer.js, prompts, Chalk, Ora, Ink, citty, Clipanion, Gluegun (JS/TS), Cobra, urfave/cli, pflag, Kong, Bubbletea, Lip Gloss, Huh, go-flags (Go), clap, StructOpt, argh, dialoguer, indicatif, console, Ratatui (Rust), picocli, JCommander, Airline, Spring Shell (Java)
- Configuration management detection: python-dotenv, Dynaconf, Hydra, OmegaConf, Pydantic Settings, python-decouple, environs, Everett, Confuse, ConfigObj (Python), .env/.env.example file detection, dotenv, Convict, node-config, envalid, env-cmd, cross-env, nconf, cosmiconfig, rc, t3-env (JS/TS), Viper, envconfig, godotenv, koanf, env, cleanenv (Go), config-rs, dotenvy, Figment, envy (Rust), Spring Config, Typesafe Config, Commons Configuration, dotenv-java (Java)
- Caching library detection: redis-py, cachetools, DiskCache, django-redis, Flask-Caching, aiocache, cashews, dogpile.cache, pymemcache, pylibmc, CacheControl (Python), ioredis, redis (Node), node-cache, lru-cache, Keyv, cache-manager, Memcached (Node), catbox (JS/TS), go-redis, Ristretto, BigCache, groupcache, FreeCache, GCache, gomemcache (Go), moka, cached, redis-rs, mini-moka (Rust), Caffeine, Ehcache, Spring Cache, Jedis, Lettuce, Redisson, Guava Cache, Hazelcast (Java)
- Template engine detection: Jinja2, Mako, Chameleon, Genshi, Cheetah, Django Templates (Python), Handlebars, EJS, Pug, Nunjucks, Mustache, Liquid, Eta, Marko, Edge.js, Vue SFC, Svelte, Solid, Astro (JS/TS), Pongo2, Raymond, Jet, Amber (Go), Tera, Askama, Handlebars (Rust), MiniJinja, Maud (Rust), Thymeleaf, FreeMarker, Velocity, Mustache (Java), Pebble (Java)
- Serialization format detection: Protocol Buffers, MessagePack, Apache Avro, Apache Thrift, FlatBuffers, CBOR, YAML, TOML, orjson, ujson, Pydantic, Marshmallow, cattrs, Pickle, Apache Arrow, Parquet, BSON (Python), protobufjs, js-yaml, superjson, Apache Arrow (JS/TS), Protocol Buffers, MessagePack, YAML, TOML, go-json (Go), serde_json, simd-json, Bincode, Postcard (Rust), Jackson, Gson, Kryo (Java) — via deps, config files, .proto/.avsc files
- Dependency injection detection: dependency-injector, python-inject, Lagom, punq, wireup, svcs, dishka, FastAPI Depends (Python), InversifyJS, tsyringe, TypeDI, Awilix, BottleJS, injection-js, Angular DI, NestJS DI (JS/TS), Uber Fx, Uber Dig, Wire, do (Go), Shaku, inject (Rust), Spring DI, Google Guice, Dagger, CDI, Micronaut DI, Quarkus CDI (Java)
- WebSocket library detection: websockets, python-socketio, Django Channels, Starlette WebSocket, Tornado WebSocket, Autobahn, aiohttp WebSocket, wsproto (Python), Socket.IO, ws, SockJS, Primus, tRPC WebSocket, graphql-ws, Pusher, Ably, Action Cable, Centrifugo (JS/TS), Gorilla WebSocket, nhooyr/websocket, gobwas/ws, Melody (Go), Tungstenite, Axum/Actix/Warp WebSocket (Rust), Spring WebSocket, Jakarta WebSocket, Tyrus, Netty WebSocket (Java)
- GraphQL library detection: Graphene, Graphene-Django, Ariadne, Strawberry, sgqlc, gql, graphql-core, Tartiflette (Python), graphql-js, Apollo Server, Apollo Client, GraphQL Yoga, TypeGraphQL, Nexus, GraphQL Code Generator, graphql-request, URQL, Relay, Mercurius, Pothos, graphql-tools, graphql-tag (JS/TS), gqlgen, graphql-go, graph-gophers, Thunder, genqlient (Go), Juniper, async-graphql, graphql-client, Cynic (Rust), graphql-java, GraphQL Spring, Netflix DGS, SmallRye GraphQL, graphql-kotlin (Java) — also detects .graphql/.gql schema files
- Event streaming detection: Confluent Kafka, kafka-python, aiokafka, RabbitMQ (pika/aio-pika), Kombu, NATS, Apache Pulsar, Faust (Python), KafkaJS, RabbitMQ (amqplib), NATS, BullMQ, Google Pub/Sub, AWS SQS/SNS/Kinesis, Azure Event Hubs/Service Bus (JS/TS), kafka-go, Sarama, Watermill, NATS (Go), rdkafka, RabbitMQ (lapin), NATS (Rust), Spring Kafka/AMQP, Kafka Clients (Java)
- Payment & billing detection: Stripe, PayPal, Braintree, Square, Adyen, Paddle, Razorpay, Mollie, Coinbase Commerce, GoCardless, Paystack, Flutterwave, Lemon Squeezy (Python), Stripe, PayPal, Braintree, Square, Adyen, Paddle, Razorpay, Mollie, Recurly, Chargebee, Lemon Squeezy (JS/TS), Stripe, PayPal, Braintree, Adyen, Razorpay (Go), async-stripe (Rust), Stripe, PayPal, Braintree, Adyen, Square, Razorpay (Java)
- Date & time library detection: Arrow, Pendulum, python-dateutil, pytz, humanize, dateparser, iso8601, ciso8601 (Python), Day.js, date-fns, Luxon, Moment.js, Spacetime, Temporal, timeago.js, chrono-node (JS/TS), jinzhu/now, dateparse (Go), chrono, time (Rust), Joda-Time, ThreeTen-Extra, PrettyTime (Java)
- Image processing library detection: Pillow, OpenCV, scikit-image, imageio, Wand, CairoSVG, pyvips, rawpy (Python), Sharp, Jimp, node-canvas, napi-canvas, GraphicsMagick, image-size, pngjs, pixelmatch, BlurHash, Plaiceholder, IMG.LY, Cropper.js (JS/TS), imaging, gg, nfnt/resize, bild, GoCV, x/image (Go), image, imageproc, resvg, OpenCV (Rust), Thumbnailator, imgscalr, TwelveMonkeys, Scrimage (Java)
- Cryptography library detection: cryptography, PyCryptodome, PyNaCl, bcrypt, Passlib, Argon2, pyOpenSSL (Python), CryptoJS, bcrypt.js, jose, node-forge, TweetNaCl, libsodium, OpenPGP.js, noble-curves/hashes (JS/TS), x/crypto, age, CIRCL (Go), ring, rustls, Orion, sha2, aes-gcm (Rust), Bouncy Castle, Tink, Jasypt (Java)
- PDF & document library detection: ReportLab, WeasyPrint, xhtml2pdf, pypdf, PyMuPDF, pdfplumber, PDFMiner, python-docx, openpyxl, XlsxWriter (Python), jsPDF, pdf-lib, PDFKit, pdfmake, React-PDF, ExcelJS, SheetJS, PapaParse (JS/TS), Excelize, UniPDF, gofpdf (Go), printpdf, genpdf, lopdf (Rust), iText, Apache PDFBox, OpenPDF, JasperReports, Apache POI (Java)
- Data visualization library detection: Matplotlib, Plotly, Seaborn, Bokeh, Altair, Dash, Streamlit, Gradio, pyecharts, Plotext (Python), D3.js, Chart.js, Recharts, Nivo, Victory, Visx, ECharts, Highcharts, ApexCharts, Three.js, Deck.gl, Tremor, Vega/Vega-Lite (JS/TS), go-echarts, Gonum Plot, go-chart, termui (Go), Plotters, plotlib, charming (Rust), JFreeChart, XChart, JavaFX Charts (Java)
- Geospatial & mapping library detection: GeoPandas, Shapely, Fiona, rasterio, pyproj, GDAL, geopy, GeoAlchemy2, H3, Cartopy, OSMnx, xarray (Python), Leaflet, Mapbox GL, MapLibre GL, OpenLayers, Cesium, Turf.js, Google Maps, react-map-gl, H3-js (JS/TS), orb, S2 Geometry, go-geom, Tile38, H3 (Go), geo, geozero, proj, H3, S2 (Rust), GeoTools, JTS, Spatial4j, H3, GraphHopper (Java)
- Audio/video & media library detection: FFmpeg, MoviePy, Pydub, Librosa, SoundFile, PyAudio, PyAV, torchaudio, Essentia, music21 (Python), fluent-ffmpeg, Tone.js, Howler.js, Video.js, HLS.js, Shaka Player, Mediasoup, PeerJS (JS/TS), Beep, Oto, Ebiten, GoAV (Go), Rodio, CPAL, Symphonia, GStreamer (Rust), JavaCV, JCodec, TarsosDSP (Java)
- Math & scientific computing library detection: NumPy, SciPy, SymPy, Pandas, Polars, scikit-learn, Numba, Dask, JAX, PyMC, CVXPY (Python), math.js, Danfo.js, Arquero, TensorFlow.js (JS/TS), Gonum, stats (Go), nalgebra, ndarray, statrs, Linfa (Rust), Commons Math, EJML, ND4J, Smile, Tablesaw (Java)
- Concurrency & async library detection: Twisted, trio, AnyIO, Gevent, uvloop, Curio, Celery, aiofiles (Python), RxJS, p-queue, p-limit, Bluebird, workerpool, threads.js, Comlink, Piscina, Tinypool (JS/TS), x/sync, conc, ants, pond (Go), Tokio, async-std, smol, Rayon, Crossbeam (Rust), RxJava, Project Reactor, Akka, Vert.x (Java)
- Compression & archive library detection: Zstandard, LZ4, Brotli, Snappy, Blosc, 7-Zip, RAR (Python), pako, fflate, JSZip, archiver (JS/TS), klauspost/compress, pgzip (Go), flate2, Zstandard, Brotli, Snappy (Rust), Commons Compress, Snappy, LZ4, Zip4j (Java)
- Email & SMTP library detection: SendGrid, Mailgun, Postmark, Resend, django-anymail, Flask-Mail, yagmail, aiosmtplib, Mailchimp (Python), Nodemailer, SendGrid, Resend, MJML, React Email (JS/TS), Gomail, go-smtp (Go), Lettre, mail-send (Rust), JavaMail, Jakarta Mail, Spring Mail, Commons Email (Java)
- Accessibility & a11y tool detection: axe-core, Playwright, Selenium, Pa11y (Python), axe-core, jsx-a11y, React Aria, Radix UI, Reach UI, Downshift, react-focus-lock, focus-trap-react, Pa11y, Lighthouse, Testing Library, jest-axe, vitest-axe, cypress-axe, ally.js, a11y-dialog, vue-a11y-utils (JS/TS), .accessibilityrc, .pa11yci config files
- Web scraping & crawling detection: Scrapy, BeautifulSoup, lxml, Parsel, MechanicalSoup, requests-html, selectolax, trafilatura, newspaper3k (Python), Puppeteer, Playwright, Cheerio, Crawlee, x-ray, jsdom, node-html-parser, linkedom, happy-dom (JS/TS), Colly, goquery, chromedp, rod (Go), scraper, select.rs, spider, headless_chrome (Rust), jsoup, HtmlUnit, WebMagic, crawler4j, Apache Nutch (Java)
- Desktop & cross-platform framework detection: PyQt5/6, PySide2/6, wxPython, Kivy, DearPyGui, CustomTkinter, Flet, PySimpleGUI, Toga, Textual, pyglet, Tkinter (Python), Electron, Tauri, NW.js, Neutralino, Capacitor, React Native, Ionic (JS/TS), Fyne, Wails, Gio (Go), Iced, Dioxus, Slint, egui, druid, Tauri, gtk-rs (Rust), JavaFX, Swing, SWT, Compose Desktop (Java), tauri.conf.json, src-tauri directory
- File storage & object store detection: boto3, aioboto3, s3fs, google-cloud-storage, gcsfs, azure-storage-blob, minio, cloudinary, django-storages, flask-uploads, python-magic, smart-open (Python), @aws-sdk/client-s3, aws-sdk, @google-cloud/storage, @azure/storage-blob, minio, cloudinary, uploadthing, @vercel/blob, @supabase/storage-js, multer, formidable, busboy, @cloudflare/r2, firebase/storage (JS/TS), aws-sdk-go, cloud.google.com/go/storage, azure-storage-blob-go, minio/minio-go (Go), aws-sdk-s3, rusoto_s3, cloud-storage, object_store (Rust), aws+s3, google-cloud-storage, azure-storage-blob, minio (Java)
- Form library detection: wtforms, flask-wtf, django-crispy-forms, django-formtools (Python), react-hook-form, formik, final-form, @tanstack/react-form, conform-to, react-jsonschema-form, uniforms, vee-validate, formkit, vuelidate, react-aria, angular/forms, svelte-forms-lib, felte, sveltekit-superforms (JS/TS)
- Animation library detection: Manim, pyglet, Arcade (Python), Framer Motion, GSAP, anime.js, Lottie, react-spring, Motion One, AutoAnimate, Rive, Popmotion, Theatre.js, Velocity.js, VueUse Motion, AnimXYZ, React Transition Group, Svelte Motion, Vue Kinesis (JS/TS), keyframe, interpolation (Rust)
- Routing library detection: Flask Routes, FastAPI Router, Django URLs, Starlette/aiohttp/Sanic/Falcon/Bottle Routes (Python), React Router, TanStack Router, Vue Router, Angular Router, Wouter, SvelteKit Router, Expo Router, React Navigation, Navigo, Reach Router (JS/TS), Gorilla Mux, Chi, Gin Router, Echo Router, Fiber Router, httprouter (Go), Axum/Actix Web/Warp/Rocket Router (Rust), Spring MVC/WebFlux Router, Javalin Router, Spark Java Router (Java)
- Game development framework detection: Pygame, Arcade, pyglet, Panda3D, Ursina, Pyxel, Cocos2d, Ren'Py (Python), Phaser, PixiJS, Three.js, Babylon.js, Kaboom.js, Excalibur, melonJS, PlayCanvas, A-Frame, Matter.js, Cannon.js, Planck.js (JS/TS), Ebiten, Pixel, g3n (Go), Bevy, ggez, macroquad, Piston, Amethyst, Fyrox, Tetra (Rust), LibGDX, LWJGL, jMonkeyEngine, Slick2D (Java)
- CMS & headless CMS detection: Wagtail, django CMS, Mezzanine, Pelican, Lektor, Nikola (Python), Strapi, Sanity, Contentful, Ghost, KeystoneJS, Payload CMS, Directus, TinaCMS, Contentlayer, Nextra, Builder.io, Storyblok, Prismic, WordPress, Decap CMS, Hygraph (JS/TS), Hugo (Go/config), Jekyll (Ruby) — via deps, config files, and directory markers
- Rate limiting detection: SlowAPI, Flask-Limiter, django-ratelimit, django-axes, Limits, aiolimiter (Python), express-rate-limit, rate-limiter-flexible, NestJS Throttler, Bottleneck, Upstash Ratelimit, express-slow-down (JS/TS), Tollbooth, go-limiter, x/time/rate (Go), Governor, actix-limitation, tower-rate-limit (Rust), Bucket4j, Resilience4j, Guava RateLimiter (Java)
- Database migration detection: Alembic, Django Migrations, Yoyo, Aerich, Piccolo Migrations (Python), Prisma Migrate, Drizzle Kit, Knex/TypeORM/Sequelize/MikroORM Migrations, db-migrate, Umzug (JS/TS), golang-migrate, Goose, sql-migrate, dbmate (Go), Diesel/SeaORM/sqlx Migrations, Refinery (Rust), Flyway, Liquibase, MyBatis Migrations (Java)
- gRPC & RPC framework detection: gRPC, betterproto, Apache Thrift, RPyC, Pyro5, zerorpc, JSON-RPC (Python), tRPC, ConnectRPC, nice-grpc, Mali (JS/TS), Twirp, rpcx (Go), Tonic, tarpc, Cap'n Proto, Prost (Rust), Apache Dubbo, Apache Avro RPC (Java), Protobuf (.proto files)
- Code generation tool detection: protoc, datamodel-code-generator, Cookiecutter, Copier (Python), GraphQL Codegen, OpenAPI Generator, openapi-typescript, ts-proto, Buf, Plop, Hygen, Prisma Generate (JS/TS), sqlc, gqlgen, oapi-codegen, Ent (Go), Prost Build, Tonic Build, bindgen, cbindgen (Rust), MapStruct, Lombok, jOOQ Codegen, Immutables (Java)
- Mocking & test fixture detection: pytest-mock, responses, HTTPretty, VCR.py, FreezeGun, Faker, Factory Boy, Hypothesis, Moto (Python), MSW, nock, Sinon.js, Faker.js, Fishery, Mirage JS (JS/TS), testify, gomock, httpmock, GoFakeIt (Go), mockall, wiremock-rs, fake-rs, proptest (Rust), Mockito, WireMock, Testcontainers (Java)
- Changelog & release tool detection: Commitizen, Towncrier, bump2version, setuptools-scm (Python), semantic-release, Changesets, release-it, Lerna, release-please (JS/TS), GoReleaser (Go), cargo-release, cargo-dist (Rust), Maven Release Plugin (Java), config files (.releaserc, .changeset, cliff.toml, CHANGELOG.md)
- E2E & browser testing detection: Selenium, Playwright, Splinter, Behave, Locust, Appium (Python), Cypress, WebdriverIO, Puppeteer, TestCafe, Nightwatch, Detox, CodeceptJS (JS/TS), chromedp, Rod (Go), thirtyfour, fantoccini (Rust), Selenide, Cucumber, Karate, REST Assured (Java), config files (cypress.config, playwright.config)
- Monorepo tool detection: Nx, Turborepo, Lerna, Changesets, Rush, Moon, pnpm Workspaces (JS/TS), Bazel, Pants, Buck2 (polyglot), Go Workspaces (Go), Cargo Workspaces (Rust), config files (nx.json, turbo.json, lerna.json, rush.json, pnpm-workspace.yaml)
- Error tracking & APM detection: Sentry, Datadog APM, New Relic, Elastic APM, OpenTelemetry, Rollbar, Bugsnag, Honeybadger, Airbrake, Pyroscope (Python), LogRocket, Highlight, AppSignal (JS/TS), across Go/Rust/Java
- Static site generator detection: MkDocs, Sphinx, Pelican, Nikola, Lektor (Python), Next.js, Gatsby, Astro, Nuxt, SvelteKit, Eleventy, VitePress, VuePress, Docusaurus, Remix, Hexo (JS/TS), Hugo (Go), Jekyll, Middleman (Ruby), config files
- Analytics & product analytics detection: PostHog, Mixpanel, Amplitude, Segment, Plausible, RudderStack, Countly (Python), Google Analytics, Heap, FullStory, Hotjar, Pirsch, Umami, Vercel Analytics (JS/TS), across Go/Java
- Mobile framework detection: React Native, Expo, Ionic, Capacitor, NativeScript, Tauri, Quasar (JS/TS), Flutter (Dart), Kotlin Multiplatform, Android (Native), Swift Package, Xcode, .NET MAUI, Xamarin, config files
- **Shipped**: N-01, N-17, N-19, N-21, N-24, N-28, N-31, N-34, N-37, N-41, N-43, N-47, N-50, N-52, N-55, N-58, N-61, N-64, N-67, N-70, N-73, N-76, N-79, N-82, N-85, N-88, N-90, N-93, N-96, N-99, N-102, N-105, N-108, N-111, N-114, N-117, N-120, N-123, N-126, N-129, N-132, N-135, N-138, N-141, N-145, N-146, N-148, N-151, N-154, N-157, N-160, N-163, N-167, N-169, N-172, N-175, N-180, N-181, N-182, N-183, N-184, N-185, N-186, N-187, N-188, N-189, N-190, N-191, N-192, N-193, N-194, N-195, N-196, N-197, N-198, N-199

### INTELLIGENCE — "See what others miss"
- Health scoring across 4 dimensions (tests/git/docs/structure)
- Cross-project pattern detection (shared deps, version mismatches, health gaps)
- Side-by-side project comparison with actionable insights
- Cross-project infrastructure intelligence (shared infra, divergence, gaps)
- Cross-project security intelligence (shared tools, adoption gaps, divergence)
- Cross-project quality intelligence (shared tools, adoption gaps, linter divergence)
- Cross-project AI/ML intelligence (shared tools, LLM provider divergence, experiment tracking gaps)
- Cross-project testing intelligence (shared frameworks, runner divergence, testing gaps)
- Cross-project database intelligence (shared databases, relational/vector/broker divergence, database gaps)
- Cross-project package manager intelligence (shared managers, JS/Python/Java divergence)
- Cross-project license intelligence (shared licenses, copyleft/permissive divergence, license gaps)
- Cross-project documentation intelligence (shared artifacts, docs coverage divergence, README/CHANGELOG/CONTRIBUTING gaps)
- Cross-project CI/CD configuration intelligence (shared config, dep update strategy divergence, PR template/CODEOWNERS/pre-commit gaps)
- Cross-project runtime version intelligence (shared versions, version divergence, pinning gaps)
- Cross-project build tool intelligence (shared tools, Python/Java divergence, automation gaps)
- Cross-project API specification intelligence (shared specs, REST/GraphQL/RPC paradigm divergence, API spec gaps)
- Cross-project monitoring intelligence (shared tools, error tracker divergence, APM divergence, monitoring gaps)
- Cross-project authentication intelligence (shared auth tools, auth provider divergence, session-vs-token strategy divergence, auth gaps for web projects)
- Cross-project messaging intelligence (shared messaging tools, email provider divergence, real-time/push divergence, messaging gaps for web projects)
- Cross-project deployment target intelligence (shared targets, serverless/edge vs container PaaS vs IaC divergence, deploy gaps for web projects)
- Cross-project state management intelligence (shared libraries, flux/proxy/atomic/machine paradigm divergence, state management gaps for frontend projects)
- Cross-project CSS/styling intelligence (shared frameworks, utility-first/CSS-in-JS/component library paradigm divergence, CSS gaps for frontend projects)
- Cross-project bundler intelligence (shared bundlers, modern/fast vs traditional vs library generation divergence, bundler gaps for JS/TS projects)
- Cross-project ORM intelligence (shared ORM/DB clients, ORM vs raw client paradigm divergence, ORM gaps for projects with databases)
- Cross-project i18n intelligence (shared i18n tools, ICU/message format vs key-based vs extraction-based divergence, i18n gaps for web projects)
- Cross-project validation intelligence (shared validation tools, schema-first vs model/decorator-based vs form validation divergence, validation gaps for API/backend projects)
- Cross-project logging intelligence (shared logging tools, structured vs traditional logging divergence, logging gaps for backend projects)
- Cross-project container orchestration intelligence (shared orchestration tools, IaC vs Kubernetes-native vs Compose divergence, orchestration gaps for Docker projects)
- Cross-project cloud provider intelligence (shared providers, hyperscaler vs edge/PaaS divergence, multi-hyperscaler complexity warnings, cloud gaps for deployed projects)
- Cross-project task queue intelligence (shared task queues, traditional vs workflow vs cron paradigm divergence, task queue gaps for backend projects)
- Cross-project search engine intelligence (shared search engines, server-side vs client-side vs SaaS paradigm divergence, search gaps for database-backed projects)
- Cross-project feature flag intelligence (shared flag tools, SaaS vs self-hosted vs analytics paradigm divergence, feature flag gaps for web projects)
- Cross-project HTTP client intelligence (shared HTTP clients, sync vs async vs fetch-based vs RPC-style paradigm divergence, HTTP client gaps for backend projects)
- Cross-project documentation generation intelligence (shared doc generators, static-site vs API-docs vs component-docs paradigm divergence, doc generator gaps for projects with 20+ source files)
- Cross-project CLI framework intelligence (shared CLI frameworks, declarative vs TUI paradigm divergence)
- Cross-project configuration management intelligence (shared config tools, env-based vs structured paradigm divergence, config tool gaps for backend projects)
- Cross-project caching intelligence (shared caching tools, Redis-based vs in-memory paradigm divergence, caching gaps for backend projects with databases)
- Cross-project template engine intelligence (shared template engines, string-based vs component-based paradigm divergence)
- Cross-project serialization format intelligence (shared serialization formats, binary vs text-based paradigm divergence)
- Cross-project DI framework intelligence (shared DI frameworks, container-based vs implicit paradigm divergence)
- Cross-project WebSocket intelligence (shared WebSocket libs, managed vs self-hosted paradigm divergence)
- Cross-project GraphQL intelligence (shared GraphQL libs, server-first vs client-first paradigm divergence)
- Cross-project event streaming intelligence (shared streaming tools, kafka-based vs amqp-based vs cloud-managed paradigm divergence)
- Cross-project payment intelligence (shared payment tools, traditional vs merchant-of-record paradigm divergence)
- Cross-project date/time intelligence (shared date/time libs, modern vs legacy paradigm divergence)
- Cross-project image processing intelligence (shared image libs, high-level vs low-level paradigm divergence)
- Cross-project data visualization intelligence (shared viz libs, interactive/dashboard vs static/notebook paradigm divergence)
- Cross-project geospatial intelligence (shared geo libs, mapping/visualization vs analysis/computation paradigm divergence)
- Cross-project media intelligence (shared media libs, audio processing vs video/streaming paradigm divergence)
- Cross-project math/scientific computing intelligence (shared math libs, numerical/array vs statistical/ML paradigm divergence)
- Cross-project async/concurrency intelligence (shared async libs, reactive vs parallel paradigm divergence)
- Cross-project cryptography intelligence (shared crypto libs, high-level/password hashing vs low-level/primitives paradigm divergence)
- Cross-project PDF/document intelligence (shared PDF libs, generation/creation vs parsing/extraction paradigm divergence)
- Cross-project email intelligence (shared email libs, SaaS/API-based vs SMTP/self-hosted paradigm divergence)
- Cross-project compression intelligence (shared compression libs, archival/format vs streaming/fast paradigm divergence)
- Cross-project a11y intelligence (shared a11y tools, testing/auditing vs component/runtime paradigm divergence)
- Cross-project scraping intelligence (shared scraping libs, browser-based vs parser-based paradigm divergence)
- Cross-project desktop framework intelligence (shared desktop frameworks, native toolkit vs web-wrapped paradigm divergence)
- Cross-project file storage intelligence (shared file storage tools, cloud-native vs dev-platform paradigm divergence)
- Cross-project form library intelligence (shared form libs, schema-driven vs imperative paradigm divergence)
- Cross-project animation library intelligence (shared animation libs, declarative vs imperative paradigm divergence)
- Cross-project routing library intelligence (shared routing libs, framework-integrated vs standalone paradigm divergence)
- Cross-project game framework intelligence (shared game frameworks, 2D vs 3D paradigm divergence)
- Cross-project CMS intelligence (shared CMS tools, headless/API-first vs traditional/monolithic paradigm divergence)
- Cross-project rate limiter intelligence (shared rate limiters, middleware vs library paradigm divergence)
- Cross-project database migration intelligence (shared migration tools, ORM-integrated vs standalone paradigm divergence)
- Cross-project gRPC/RPC intelligence (shared RPC libs, schema-based vs dynamic paradigm divergence)
- Cross-project code generation intelligence (shared codegen tools, schema-driven vs template-driven paradigm divergence)
- Cross-project mocking intelligence (shared mocking libs, HTTP/service mocking vs unit/object mocking paradigm divergence)
- Cross-project release tool intelligence (shared release tools, automated vs manual release paradigm divergence)
- Cross-project E2E testing intelligence (shared E2E tools, modern vs traditional paradigm divergence)
- Cross-project monorepo intelligence (shared monorepo tools, JS-native vs polyglot paradigm divergence)
- Cross-project error tracking intelligence (shared error trackers, hosted vs agent-based paradigm divergence)
- Cross-project SSG intelligence (shared static site generators, app-framework vs docs-focused paradigm divergence)
- Cross-project analytics intelligence (shared analytics tools, privacy-first vs commercial paradigm divergence)
- Cross-project mobile framework intelligence (shared mobile frameworks, cross-platform JS vs native/cross-native paradigm divergence)
- **Shipped**: N-02, N-03, N-15, N-18, N-23, N-25, N-27, N-29, N-32, N-35, N-38, N-42, N-45, N-48, N-51, N-53, N-56, N-59, N-62, N-65, N-68, N-71, N-74, N-77, N-80, N-83, N-86, N-89, N-91, N-94, N-97, N-100, N-103, N-106, N-109, N-112, N-115, N-118, N-121, N-124, N-127, N-131, N-134, N-139, N-142, N-144, N-149, N-152, N-155, N-158, N-161, N-164, N-166, N-170, N-173, N-176, N-178, N-179, N-180, N-181, N-182, N-183, N-184, N-185, N-186, N-187, N-188, N-189, N-190, N-191, N-192, N-193, N-194, N-195, N-196, N-197, N-198, N-199

### EXPERIENCE — "Beautiful enough to screenshot"
- Rich terminal dashboard with tables, progress bars, color
- Fast scanning (31s for 8 projects, 1.2M LOC)
- Scan history & health trends over time
- Persistent TOML configuration
- Portfolio summary panel: language distribution, framework adoption, infra coverage, security posture
- Rich markdown export for portfolio reports
- Enhanced doctor recommendations leveraging all detection data
- Testing framework adoption in portfolio summary panel and markdown export
- Database adoption in portfolio summary panel and markdown export
- Package manager adoption in portfolio summary panel and markdown export
- License distribution in portfolio summary panel and markdown export
- Comprehensive JSON export with connections, recommendations, and portfolio aggregates
- Filterable dashboard: `atlas status --grade A --lang Python --has Docker --min-health 80`
- Quick insights: top 3 actionable recommendations shown inline in `atlas status` dashboard
- CSV export: `atlas export --format csv` for spreadsheet-friendly portfolio data
- Health trend sparklines: Unicode mini-charts in `atlas status` showing per-project health history
- Markdown badge generation: shields.io badges for portfolio README (health grade, project count, test files, LOC, primary language)
- Connection category filtering: `atlas connections --type security` to filter cross-project intelligence by category (19 categories)
- Connection statistics panel: summary of total connections, severity breakdown (critical/warning/info), top categories by count
- Export format auto-detection: `atlas export -o report.json` auto-detects format from file extension (.md/.json/.csv)
- Doctor category summary: `atlas doctor` shows recommendation category breakdown (e.g., "3 security, 2 testing, 1 infra") after priority summary
- Connection category list: `atlas connections --type list` shows all available categories with their connection types
- Export connection summary stats: markdown exports show "N connections: X warning, Y info" header, JSON exports include connection_summary with total/critical/warning/info counts
- Connection severity filtering: `atlas connections --severity warning` filters connections by severity level (info, warning, critical)
- Project search: `atlas search <term>` finds projects by name, language, framework, or technology. Shows matches with health grade and tech summary
- Batch remove: `atlas batch-remove` prunes stale projects whose directories no longer exist on disk. Lists removed projects with paths, auto-saves portfolio
- Rename project: `atlas rename <old> <new>` renames a project in the portfolio. Prevents name collisions
- Top projects command: `atlas top --by health|loc|tests|commits -n 5` shows top N projects ranked by metric
- Version command: `atlas version` shows installed version
- Export filtering: `atlas export --grade A --lang Python --has Docker --min-health 80 --max-health 100` filters projects in any export format (markdown/json/csv)
- Doctor JSON export: `atlas doctor --format json` outputs structured JSON with recommendations array, priority/category summary counts for CI integration
- Connections JSON export: `atlas connections --format json` outputs structured JSON with connections array (type, detail, projects, severity), total count, severity summary for CI integration
- Connections CSV export: `atlas connections --format csv` outputs CSV with Type, Detail, Projects, Severity columns. Works with --type and --severity filters
- Doctor CSV export: `atlas doctor --format csv` outputs CSV with Priority, Category, Message, Projects columns for spreadsheet analysis
- Status JSON export: `atlas status --format json` outputs structured JSON with project array (name, path, health grades/scores, languages, frameworks, LOC, files, license). Works with all filters
- Compare JSON export: `atlas compare A B --format json` outputs structured JSON with project_a/project_b summaries (health, metrics, languages, frameworks), deltas (health_percent, loc, source_files, test_files, commits), shared/unique frameworks and deps
- Top projects JSON export: `atlas top --format json` outputs structured JSON with metric, limit, and projects array (rank, name, value, health_grade, stack). Works with --by and --limit options
- Search JSON export: `atlas search <term> --format json` outputs structured JSON with query, total count, and projects array (name, path, health_grade, health_percent, languages, frameworks, loc, license)
- Doctor category filter: `atlas doctor --category tests` filters recommendations by category (tests, docs, git, infra, quality, security, structure, deps). Works with all output formats (rich, json, csv)
- Connections project filter: `atlas connections --project myapp` filters connections to only those involving a specific project. Works with all output formats and combines with --type and --severity filters
- Connections summary mode: `atlas connections --summary` shows compact category-by-count table with severity breakdown. Supports `--format json` for structured output. Works with all filters (--type, --severity, --project)
- Doctor priority filter: `atlas doctor --priority critical` filters recommendations by priority level (critical, high, medium, low). Works with all output formats (rich, json, csv) and combines with --category filter
- Status grade distribution: `atlas status --grades` shows compact grade distribution bar chart (A/B+/B/C/D/F counts with Unicode bars). Supports `--format json` for structured output. Works with all existing filters
- Status CSV export: `atlas status --format csv` outputs CSV with Name, Path, Grade, Health%, Tests%, Git%, Docs%, Structure%, Languages, Frameworks, LOC, Source Files, Test Files, License columns. Works with all filters
- Compare CSV export: `atlas compare A B --format csv` outputs CSV with Metric/A/B/Delta columns. Rows: Grade, Health%, Tests%, Git%, Docs%, Structure%, LOC, Source Files, Test Files, Commits, Languages, Frameworks, License
- Top projects CSV export: `atlas top --format csv` outputs CSV with Rank, Name, metric value, Grade, Stack columns. Works with --by and --limit options
- Status sort: `atlas status --sort name|health|loc|grade` sorts project list. Works with all filters and output formats (rich, json, csv)
- Connections sort: `atlas connections --sort type|severity|projects` sorts connections. Works with all filters and output formats (rich, json, csv)
- Doctor sort: `atlas doctor --sort priority|category` sorts recommendations. Works with all filters and output formats (rich, json, csv)
- Search sort: `atlas search <term> --sort name|health|loc` sorts search results. By name (alphabetical), health (descending), or LOC (descending). Works with JSON output format
- Export sort: `atlas export --sort name|health|loc` sorts projects in export output. Works with all formats (markdown, json, csv) and all filters
- Top projects filter: `atlas top --lang Python --has Docker` filters which projects are eligible for ranking. Works with all metrics, formats, and --limit
- Doctor project filter: `atlas doctor --project myapp` filters recommendations to only those involving a specific project. Works with all output formats (rich, json, csv) and combines with --category and --priority filters
- Search result limit: `atlas search <term> --limit 5` limits the number of search results displayed. Works with all output formats and combines with --sort
- Connections result limit: `atlas connections --limit 10` limits the number of connections displayed. Applied after filters and sorting. Works with all output formats (rich, json, csv), --summary, and all filters
- Doctor result limit: `atlas doctor --limit 5` limits the number of recommendations displayed. Applied after filters and sorting. Works with all output formats (rich, json, csv) and combines with --category, --priority, --project, and --sort
- Export result limit: `atlas export --limit 5` limits the number of projects in export output. Applied after filters and sorting. Works with all output formats (markdown, json, csv) and combines with --grade, --lang, --has, --min-health, --max-health, and --sort
- Status result limit: `atlas status --limit 5` limits the number of projects displayed. Applied after sorting. Works with all output formats (rich, json, csv) and combines with --grade, --lang, --has, --min-health, --max-health, --sort, and --grades
- **Shipped**: N-04, N-13, N-16, N-20, N-22, N-26, N-30, N-33, N-36, N-39, N-40, N-44, N-46, N-49, N-54, N-57, N-60, N-63, N-66, N-69, N-72, N-75, N-78, N-81, N-84, N-87, N-92, N-95, N-98, N-101, N-104, N-107, N-110, N-113, N-116, N-119, N-122, N-125, N-128, N-130, N-133, N-136, N-137, N-140, N-143, N-147, N-150, N-153, N-156, N-159, N-162, N-165, N-168, N-171, N-174, N-177

### DISTRIBUTION — "Get it into hands"
- PyPI package, GitHub repo, CI pipeline
- Show HN launch, Dev.to articles, Product Hunt
- Open Core monetization (Free single-repo, Pro $49 cross-project)
- CI health gates with JSON output and exit codes
- **Shipped**: N-05, N-14 | **Next**: N-06, N-08

---

## Initiative Details

### N-01: Tech Stack Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P0
**What**: Scans repos to detect Python/TS/Rust/Go/Java stacks, frameworks, and dependencies.
**Shipped**: 2026-03-04

### N-02: Health Scoring
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P0
**What**: Scores projects across 4 health dimensions: tests, git activity, documentation, structure.
**Shipped**: 2026-03-04

### N-03: Cross-Project Patterns
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P0
**What**: Detects shared dependencies, version mismatches, and health gaps across portfolio.
**Shipped**: 2026-03-04

### N-04: Terminal Dashboard
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P0
**What**: Rich terminal UI with tables, progress bars, and color-coded health indicators.
**Shipped**: 2026-03-04

### N-05: GitHub CI
**Pillar**: DISTRIBUTION | **Status**: SHIPPED | **Priority**: P1
**What**: GitHub Actions CI pipeline. Tests on Python 3.11/3.12/3.13. All 221 passing.
**Shipped**: 2026-03-04

### N-06: PyPI Publishing
**Pillar**: DISTRIBUTION | **Status**: DECIDED | **Priority**: P0
**What**: Publish to PyPI as `nxtg-atlas`. Package builds + validates. Blocked on PyPI Trusted Publisher setup only.
**Blocker**: PyPI Trusted Publisher configuration.
**Next step**: Asif configures Trusted Publisher on pypi.org for `nxtg-ai/repoatlas` repo, then `git tag v0.2.0 && git push origin v0.2.0` — N-10 workflow handles the rest automatically.

### N-07: README + GIF Demo
**Pillar**: DISTRIBUTION | **Status**: SHIPPED | **Priority**: P1
**What**: Polished README with terminal recording GIF showing full portfolio scan.
**Shipped**: 2026-03-13. GIF recorded via asciinema + agg (271KB). Shows `atlas status`, `atlas connections`, `atlas inspect`. VHS tape also included at `demo/demo.tape`.

### N-08: Show HN Launch
**Pillar**: DISTRIBUTION | **Status**: DECIDED | **Priority**: P1
**What**: Launch on Hacker News + Reddit + Twitter same day. Product Hunt day 2-3.
**Launch kit ready**: `launch/` directory has drafted posts for Show HN, Reddit (r/Python + r/commandline), Twitter/X thread, Product Hunt listing, and a day-of checklist with metrics targets.
**Blocker**: N-06 (PyPI publish). Everything else is ready.
**Next step**: Asif reviews launch copy in `launch/`, publishes to PyPI, then executes checklist.

### N-09: Pro Tier / Monetization
**Pillar**: DISTRIBUTION | **Status**: DECIDED | **Priority**: P2
**What**: Open Core model. Free (single repo) + Pro $49 one-time (cross-project intelligence, portfolio dashboard).
**Infrastructure shipped**: `license_manager.py` (key validation, activation, feature gates), `atlas license` + `atlas activate` CLI commands, 27 tests covering key validation, activation/deactivation, status, edge cases (corrupt JSON, missing files, bad checksums). Gates NOT enforced — all features remain free. Enforcement is a product decision for Asif.
**Next step**: Asif decides payment provider (Polar.sh vs Lemon Squeezy), pricing, and when to enforce gates.

### N-10: Tag-Based Release Automation
**Pillar**: DISTRIBUTION | **Status**: SHIPPED | **Priority**: P1
**What**: GitHub Actions release workflow triggered by git tags (`v*`). Runs full test matrix, builds sdist+wheel, validates with twine check, publishes to PyPI via Trusted Publisher (OIDC), and creates GitHub Release with auto-generated notes. Replaces fragile commit-message-based publish trigger.
**Shipped**: 2026-03-13. Release flow: `git tag v0.2.0 && git push origin v0.2.0` — everything else is automated.
**Impact**: Simplifies N-06 unblock — Asif only needs to configure PyPI Trusted Publisher for `nxtg-ai/repoatlas`, then push a tag.

### N-12: Doctor — Actionable Recommendations
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas doctor` command with recommendations engine (`recommendations.py`). Analyzes per-project health (tests, git, docs, structure) and cross-project patterns (version mismatches, health focus). Outputs prioritized suggestions (critical/high/medium/low) with specific fix actions. 24 recommendation tests + 4 CLI doctor tests. Enhanced by N-26 to cover security, quality, and infrastructure.
**Shipped**: 2026-03-13. Total test count: 284 → 312. README commands table updated.

### N-13: Scan History & Trends
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas trends` command with scan history tracking (`history.py`). Each `atlas scan` saves a snapshot (health, tests, LOC, per-project grades) to `~/.atlas/history.json`. `atlas trends` compares the last two scans showing portfolio-level deltas, per-project direction (up/down/stable/new/removed), and test count changes. Capped at 100 entries. 22 history unit tests + 3 CLI trends tests.
**Shipped**: 2026-03-13. README commands table updated.

### N-14: CI Mode
**Pillar**: DISTRIBUTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas ci` command for CI/CD pipelines. Re-scans portfolio, outputs structured JSON (or summary), and exits non-zero on health violations. Supports `--min-health` (portfolio threshold) and `--min-project-health` (per-project threshold). Replaces "CI integration coming soon" FAQ with working GitHub Actions example. 6 CI tests.
**Shipped**: 2026-03-13. Total test count: 336 → 342. README commands table + FAQ updated.

### N-15: Project Comparison
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas compare <a> <b>` command for side-by-side project comparison. Shows health breakdown deltas (tests/git/docs/structure with mini bars), metrics comparison (LOC, tests, commits), tech stack overlap (shared/unique frameworks and deps), version mismatch detection, and actionable insights (which dimensions the weaker project should improve). 5 CLI tests.
**Shipped**: 2026-03-13. Total test count: 342 → 347. README commands table updated.

### N-16: Configuration File
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas config` command with persistent TOML configuration (`~/.atlas/config.toml`). View all settings, get/set individual keys. Supports `ci.min_health`, `ci.min_project_health`, `export.format`. CI command reads defaults from config when flags aren't explicitly set. Uses stdlib `tomllib` (Python 3.11+) — no new dependencies. 15 config unit tests + 5 CLI config tests.
**Shipped**: 2026-03-13. Total test count: 347 → 367. README commands table updated.

### N-17: Infrastructure Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_infrastructure()` in detector.py. Detects Docker/Compose, Kubernetes/Helm, Terraform/Pulumi/CDK, CI/CD (GitHub Actions/GitLab CI/Jenkins/CircleCI), serverless (Vercel/Netlify/Cloudflare Workers/Fly.io/Render), and cloud providers (AWS/GCP/Azure from SDK deps). Added `infrastructure` field to TechStack model. Shows in `atlas inspect`. 28 infrastructure tests.
**Shipped**: 2026-03-13. Total test count: 367 → 395. README "What It Detects" table expanded.

### N-21: AI/ML Tooling Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_ai_tools()` in detector.py. Detects AI/ML frameworks and tools across Python (Anthropic, OpenAI, LangChain, LlamaIndex, Transformers, PyTorch, TensorFlow, scikit-learn, MLflow, W&B, ChromaDB, Pinecone, Sentence Transformers) and JavaScript (@anthropic-ai/sdk, openai, LangChain, Vercel AI SDK, Hugging Face). Also detects Jupyter notebooks (.ipynb), ML infrastructure (MLproject, wandb/, DVC). Added `ai_tools` field to TechStack model. Shows in `atlas inspect` and portfolio summary panel. 32 AI tools tests.
**Shipped**: 2026-03-13. Total test count: 451 → 483. README "What It Detects" table expanded. Directly serves North Star ("AI Engineering Teams").

### N-20: Portfolio Summary Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Aggregate portfolio insights panel added to `atlas status` dashboard (shown for 2+ projects). Displays language distribution with project counts, framework adoption (excluding Docker), infrastructure coverage (CI/CD, Docker, Cloud as X/N ratios), and security posture overview (tooling coverage, dep scanning, secret scanning). Uses Rich Panel rendering. 15 display tests.
**Shipped**: 2026-03-13. Total test count: 436 → 451. Surfaces N-17/N-19 detection data in the main dashboard.

### N-19: Security Posture Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_security_tools()` in detector.py. Detects security tooling across projects: dependency scanning (Dependabot, Renovate, Snyk), secret scanning (Gitleaks, SOPS, detect-secrets), Python SAST (Bandit, Safety, pip-audit), code analysis (CodeQL, Trivy), and security policy (SECURITY.md). Reads pre-commit configs for security hooks. Added `security_tools` field to TechStack model. Shows in `atlas inspect`. 26 security tests.
**Shipped**: 2026-03-13. Total test count: 410 → 436. README "What It Detects" table expanded.

### N-22: Rich Markdown Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Refactored markdown export into dedicated `export_report.py` module with `build_markdown_report()`. Generates comprehensive portfolio reports: header with aggregate stats, project table sorted by health, portfolio summary (languages, frameworks, infra coverage, security posture, AI/ML adoption), per-project details (health breakdown across 4 dimensions, all tech stack fields, git info), and cross-project intelligence grouped by type with severity icons. Replaces inline markdown generation in cli.py. 23 export tests.
**Shipped**: 2026-03-13. Total test count: 483 → 506. Surfaces all detection data (N-17, N-19, N-21) in exported reports.

### N-25: Quality Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project quality pattern detection via `_find_quality_patterns()` in connections.py. Analyzes quality tooling from N-24 across the portfolio to detect: shared quality tools (Ruff/mypy across 2+ projects), quality adoption gaps (no tooling, missing linting, missing type checking), and linter divergence (multiple linters across portfolio). New connection types (`shared_quality`, `quality_divergence`, `quality_gap`) displayed in `atlas connections` and markdown export. 16 quality pattern tests.
**Shipped**: 2026-03-13. Total test count: 567 → 583. Completes N-24 detection→intelligence pipeline. Parallels N-19→N-23 and N-17→N-18 patterns.

### N-24: Code Quality Tooling Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_quality_tools()` in detector.py. Detects code quality tooling across projects: Python linters (Ruff, Flake8, Pylint), Python formatters (Black, isort, autopep8), Python type checkers (mypy, Pyright), JS/TS tools (ESLint, Prettier, TypeScript, Biome), Go (golangci-lint), Rust (Clippy). Reads config files, dependency files, pyproject.toml sections, and pre-commit hooks. Added `quality_tools` field to TechStack model. Shows in `atlas inspect`, portfolio summary panel, and markdown export. 45 quality tools tests.
**Shipped**: 2026-03-13. Total test count: 522 → 567. Enables future quality intelligence layer.

### N-23: Security Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project security pattern detection via `_find_security_patterns()` in connections.py. Analyzes security tooling from N-19 across the portfolio to detect: shared security tools (Dependabot/Gitleaks across 2+ projects), security adoption gaps (no tooling, missing dep scanning, missing secret scanning), and security tool divergence (multiple dep scanners across portfolio). New connection types (`shared_security`, `security_divergence`, `security_gap`) displayed in `atlas connections` and markdown export. 16 security pattern tests.
**Shipped**: 2026-03-13. Total test count: 506 → 522. Builds on N-19 detection data. Parallels N-17→N-18 (detection→intelligence) pattern.

### N-26: Enhanced Doctor Recommendations
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Enhanced `atlas doctor` recommendations engine to leverage all detection data from N-17/N-19/N-24/N-25. Per-project: security (no tooling, missing dep scanning, missing secret scanning), quality (no tooling, missing linting, missing type checking), infrastructure (no CI/CD). Cross-project: maps security_gap/security_divergence, quality_gap/quality_divergence, infra_gap/infra_divergence connections to prioritized recommendations. 23 new recommendation tests.
**Shipped**: 2026-03-13. Total test count: 583 → 606. Surfaces all detection+intelligence data through actionable `atlas doctor` output.

### N-35: Package Manager Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project package manager pattern detection via `_find_package_manager_patterns()` in connections.py. Detects: shared package managers (Poetry/npm across 2+ projects), JS package manager divergence (npm vs Yarn vs pnpm vs Bun), Python package manager divergence (pip vs Poetry vs PDM vs uv vs Pipenv), Java build tool divergence (Maven vs Gradle). New connection types (`shared_pkg_manager`, `pkg_manager_divergence`) displayed in `atlas connections`, markdown export, and `atlas doctor`. 13 package manager pattern tests.
**Shipped**: 2026-03-21. Total test count: 736 → 749. Completes N-34 detection→intelligence pipeline. All 7 detection→intelligence pipelines complete.

### N-44: Filterable Project List
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added 5 filter options to `atlas status`: `--grade` (filter by health grade A/B+/B/C/D/F), `--lang` (filter by language), `--has` (filter by any tech — searches all TechStack fields including frameworks, databases, infrastructure, security, quality, testing, package managers, docs artifacts, CI config), `--min-health` (minimum health %), `--max-health` (maximum health %). Filters compose (AND logic). When filters active, shows "Filtered: ..." header and creates a temporary Portfolio with only matching projects. Cross-project intelligence runs on filtered set. No match shows friendly message. Helper `_project_has_tech()` does case-insensitive search across all 11 TechStack list fields. 6 new CLI integration tests.
**Shipped**: 2026-03-21. Total test count: 871 → 877. First interactive UX feature since N-16 (config).

### N-46: Dashboard Quick Insights
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Top 3 critical/high-priority recommendations shown inline in `atlas status` dashboard via new `show_quick_insights()` function in display.py. Surfaces actionable intelligence directly in the main command without requiring a separate `atlas doctor` invocation. Shows project names, recommendation icons, and a "run atlas doctor for full report" hint with remaining count. Panel hidden when no critical/high recommendations exist (healthy portfolio). Works with both filtered and unfiltered views. 7 display unit tests + 2 CLI integration tests.
**Shipped**: 2026-03-21. Total test count: 894 → 903. Bridges the gap between dashboard overview and actionable doctor recommendations.

### N-47: Runtime Version Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_runtime_versions()` in detector.py. Detects pinned runtime/language versions from config files: Python (.python-version, pyproject.toml requires-python), Node.js (.node-version, .nvmrc, package.json engines.node), Ruby (.ruby-version), Go (go.mod go directive), Rust (rust-toolchain.toml channel, rust-toolchain plain file), Java (.java-version), and multi-runtime via asdf (.tool-versions with language mapping). Priority rules: specific version files override asdf entries; .node-version overrides .nvmrc; rust-toolchain.toml overrides plain rust-toolchain. Returns `dict[str, str]` (language → version). Added `runtime_versions` field to TechStack model. Shows in `atlas inspect` project card, portfolio summary panel (display.py and export_report.py), markdown export project details, and JSON export portfolio_summary. `_project_has_tech()` searches runtime version keys. 17 detection tests.
**Shipped**: 2026-03-21. Total test count: 903 → 920. 12th detection category.

### N-52: API Specification Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_api_specs()` in detector.py. Detects API specification formats and protocols: OpenAPI/Swagger (JSON/YAML in root, docs/, api/, spec/ directories), GraphQL (schema.graphql, schema.gql, .graphqlrc configs, codegen configs, .graphql files in src/), gRPC/Protobuf (.proto files in root, proto/, protos/ directories), AsyncAPI (asyncapi.json/yaml/yml), JSON Schema (schema.json, schemas/ directory), tRPC (via @trpc/* package.json dependencies), WSDL/SOAP (.wsdl files). Returns sorted list. Added `api_specs` field to TechStack model. Shows in `atlas inspect` project card, portfolio summary panel (display.py), markdown export details and summary, JSON export portfolio_summary, and CSV export. `_project_has_tech()` searches api_specs. 20 detection tests.
**Shipped**: 2026-03-21. Total test count: 979 → 999. 14th detection category.

### N-53: API Specification Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project API specification pattern detection via `_find_api_spec_patterns()` in connections.py. Analyzes api_specs data from N-52 across the portfolio to detect: shared API specs (OpenAPI/GraphQL across 2+ projects, info), API paradigm divergence (REST vs GraphQL vs RPC across portfolio, info), and API spec gaps (projects with web frameworks like FastAPI/Django/Flask/Express but no API spec, warning). New connection types (`shared_api_spec`, `api_spec_divergence`, `api_spec_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps api_spec_gap and api_spec_divergence to `infra` recommendation categories. 16 API spec pattern tests.
**Shipped**: 2026-03-21. Total test count: 999 → 1015. Completes N-52 detection→intelligence pipeline. All 15 detection→intelligence pipelines complete.

### N-54: Health Trend Sparklines
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Unicode sparkline mini-charts in the `atlas status` dashboard showing per-project health trends over time. New `sparkline()` utility function in display.py renders float values (0.0–1.0) as Unicode block characters (▁▂▃▄▅▆▇█). `show_status()` accepts optional scan history, builds per-project health time series, and renders a "Trend" column when 2+ scan entries exist. Column hidden gracefully when no history available. CLI passes `load_history()` to `show_status()`. 10 sparkline unit tests + 7 dashboard integration tests.
**Shipped**: 2026-03-21. Total test count: 1015 → 1032. Leverages N-13 scan history data for visual trend display.

### N-55: Monitoring & Observability Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_monitoring_tools()` in detector.py. Detects monitoring, observability, error tracking, and logging tools from Python deps (sentry-sdk, ddtrace, newrelic, opentelemetry, prometheus-client, elastic-apm, bugsnag, rollbar, honeycomb, loguru, structlog), JS deps (@sentry/node, @sentry/browser, @sentry/react, @sentry/nextjs, dd-trace, newrelic, @opentelemetry/api, prom-client, @bugsnag/js, rollbar, @honeycombio/opentelemetry-node, pino, winston, @logtail/node, logrocket), Go deps (sentry-go, opentelemetry, prometheus, datadog), Rust deps (sentry, opentelemetry, tracing, prometheus), and config files (sentry.properties, .sentryclirc, newrelic.yml, datadog.yaml, prometheus.yml, otel-collector-config.yaml). Added `monitoring_tools` field to TechStack model. Shows in `atlas inspect` project card, portfolio summary panel (display.py), markdown/JSON/CSV export. `_project_has_tech()` searches monitoring_tools. 26 detection tests.
**Shipped**: 2026-03-21. Total test count: 1032 → 1058. 15th detection category.

### N-56: Monitoring & Observability Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project monitoring pattern detection via `_find_monitoring_patterns()` in connections.py. Analyzes monitoring_tools data from N-55 across the portfolio to detect: shared monitoring tools (Sentry/Datadog across 2+ projects, info), error tracker divergence (Sentry vs Bugsnag vs Rollbar vs Elastic APM across portfolio, warning), APM divergence (Datadog vs New Relic vs Elastic APM vs Honeycomb across portfolio, warning), and monitoring gaps (projects with 10+ source files but no monitoring/observability tooling, warning). New connection types (`shared_monitoring`, `monitoring_divergence`, `monitoring_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps monitoring_gap and monitoring_divergence to `infra` recommendation categories. 16 monitoring pattern tests.
**Shipped**: 2026-03-21. Total test count: 1058 → 1074. Completes N-55 detection→intelligence pipeline. All 16 detection→intelligence pipelines complete.

### N-57: Markdown Badge Generation
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas badge` command and `generate_badges()` function in cli.py. Generates shields.io-style markdown badge strings for portfolio READMEs: health grade (color-coded A=brightgreen through F=red), project count, test file count (color-coded by threshold), LOC (formatted as K/M for readability), and primary language (most common across portfolio). Supports `--output`/`-o` flag for file export. 7 CLI integration tests + 10 unit tests.
**Shipped**: 2026-03-21. Total test count: 1074 → 1091. First DISTRIBUTION-adjacent EXPERIENCE feature — helps users showcase portfolio metrics.

### N-58: Authentication & Auth Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_auth_tools()` in detector.py. Detects authentication and authorization frameworks across ecosystems: Python (Flask-Login, Flask-Security, django-allauth, DRF SimpleJWT, Authlib, PyJWT, python-jose, Passlib, FastAPI-Users, Auth0, Firebase Admin, Clerk, Supabase), JavaScript/TypeScript (NextAuth.js, Auth.js, Passport.js, express-session, jsonwebtoken, Clerk, Auth0, Firebase, Supabase Auth, Lucia, Keycloak, bcrypt, OIDC, Grant), Go (golang-jwt, Casbin, Authelia, OIDC), Rust (jsonwebtoken, OAuth2, Actix Identity, axum-login). Added `auth_tools` field to TechStack model. Shows in `atlas inspect` project card, portfolio summary panel (display.py), markdown/JSON/CSV export. `_project_has_tech()` searches auth_tools. 25 detection tests.
**Shipped**: 2026-03-21. Total test count: 1091 → 1116. 16th detection category.

### N-59: Authentication Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project authentication pattern detection via `_find_auth_patterns()` in connections.py. Analyzes auth_tools data from N-58 across the portfolio to detect: shared auth tools (Clerk/PyJWT across 2+ projects, info), auth provider divergence (Clerk vs Auth0 vs Firebase Auth vs Supabase Auth vs Keycloak across portfolio, warning), auth strategy divergence (session-based Passport.js/Flask-Login vs token-based PyJWT/NextAuth.js across portfolio, info), and auth gaps (web projects with frameworks like FastAPI/Django/Next.js but no auth tooling, warning). New connection types (`shared_auth`, `auth_divergence`, `auth_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps auth_gap and auth_divergence to `infra` recommendation categories. 17 auth pattern tests.
**Shipped**: 2026-03-21. Total test count: 1116 → 1133. Completes N-58 detection→intelligence pipeline. All 17 detection→intelligence pipelines complete.

### N-60: Connection Category Filtering
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--type`/`-t` filter option to `atlas connections` command. Filters cross-project intelligence by category: deps, health, infra, security, quality, ai, testing, database, packages, license, docs, ci, runtime, build, api, monitoring, auth (17 categories). Each category maps to its related connection types. Shows "Filtered: X/Y connections" header when active. Invalid categories show error with valid options list. `CONNECTION_CATEGORIES` dict defined in cli.py for clean mapping. 5 new CLI integration tests.
**Shipped**: 2026-03-21. Total test count: 1133 → 1138. Makes `atlas connections` output navigable for large portfolios.

### N-61: Messaging & Notification Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_messaging_tools()` in detector.py. Detects email, SMS, push notification, real-time messaging, and task queue tools across ecosystems: Python (SendGrid, Twilio, Slack SDK/Bolt, Postmark, Mailgun, Resend, Socket.IO, Pusher, Firebase Cloud Messaging, Web Push, Celery), JavaScript/TypeScript (SendGrid, Nodemailer, Resend, Twilio, Slack Web API/Bolt, Pusher, Socket.IO, Firebase Admin, BullMQ, Bull, Novu, Postmark, Web Push), Go (Gomail, Slack, Twilio), Rust (Lettre, Slack). Added `messaging_tools` field to TechStack model. Shows in `atlas inspect` project card, portfolio summary panel (display.py), markdown/JSON/CSV export. `_project_has_tech()` searches messaging_tools. 23 detection tests.
**Shipped**: 2026-03-21. Total test count: 1138 → 1161. 17th detection category.

### N-62: Messaging & Notification Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project messaging intelligence — detects shared messaging tools, email provider divergence (SendGrid/Postmark/Mailgun/Resend/Nodemailer/Gomail/Lettre), real-time/push divergence (Socket.IO/Pusher/Firebase Cloud Messaging/Web Push/Novu), and messaging gaps for web projects with frameworks but no messaging (>10 source files). Adds `_find_messaging_patterns()` to connections.py (shared_messaging, messaging_divergence, messaging_gap). Updates display.py icons/labels, export_report.py type_labels, recommendations.py type_to_category, cli.py CONNECTION_CATEGORIES. 17 connection tests.
**Shipped**: 2026-03-21. Total test count: 1161 → 1177. 19th intelligence category.

### N-63: Connection Statistics Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Summary statistics panel shown after `atlas connections` output. Displays total connection count, severity breakdown (critical/warning/info with color coding), and top 5 categories by count with "+N more" overflow. Adds `_show_connection_stats()` to display.py, called automatically from `show_connections()`. 14 tests covering all severity types, category counting, sorting, edge cases.
**Shipped**: 2026-03-21. Total test count: 1177 → 1191. 18th experience feature.

### N-64: Deployment Target Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects deployment platforms from config files and package deps. Supports 13 platforms: Vercel (vercel.json/.vercel/@vercel/node), Netlify (netlify.toml/_redirects/netlify-cli/@netlify/functions), Fly.io (fly.toml), Railway (railway.json/railway.toml), Render (render.yaml), Heroku (Procfile), Firebase Hosting (firebase.json/firebase-tools), AWS Amplify (amplify.yml/amplify/), Serverless Framework (serverless.yml), Google App Engine (app.yaml with runtime:), DigitalOcean App Platform (.do/do-app.yaml), Cloudflare Workers (wrangler.toml/wrangler), GitHub Pages (workflow detection/gh-pages dep). Adds `deploy_targets` field to TechStack. Updates models.py, detector.py, scanner.py, display.py (project card + portfolio summary), export_report.py (CSV + markdown + JSON), cli.py. 31 tests.
**Shipped**: 2026-03-21. Total test count: 1191 → 1222. 18th detection category.

### N-65: Deployment Target Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project deployment target intelligence — detects shared deploy targets, platform strategy divergence (serverless/edge vs container PaaS vs IaC serverless), and deploy gaps for web projects with frameworks but no deploy target configured (>5 source files). Adds `_find_deploy_target_patterns()` to connections.py (shared_deploy, deploy_divergence, deploy_gap). Updates display.py icons/labels, export_report.py type_labels, recommendations.py type_to_category, cli.py CONNECTION_CATEGORIES (19 categories). 17 connection tests.
**Shipped**: 2026-03-21. Total test count: 1222 → 1239. 20th intelligence category.

### N-66: Export Format Auto-Detection
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: `atlas export -o report.json` auto-detects format from file extension (.md → markdown, .json → json, .csv → csv). No `--format` flag needed when using `-o`. Unknown extensions default to markdown. Explicit `--format` overrides auto-detection. Output confirmation message now shows detected format. 7 tests.
**Shipped**: 2026-03-21. Total test count: 1239 → 1246. 19th experience feature.

### N-67: Frontend State Management Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: `detect_state_management()` in detector.py identifies frontend state management libraries from package.json dependencies. Detects 14 libraries/families: Redux (@reduxjs/toolkit, react-redux), Zustand, Recoil, Jotai, Valtio, MobX (mobx-react, mobx-react-lite), XState (@xstate/react), Pinia, Vuex, NgRx (@ngrx/store, @ngrx/effects), Signals (@preact/signals-react, @preact/signals), Effector (effector-react), Nanostores (@nanostores/react), Legend State (@legendapp/state). Returns sorted list. Integrated into models.py (TechStack field + to_dict/from_dict), scanner.py, display.py (project card + portfolio summary), export_report.py (CSV column + markdown + JSON), and cli.py (_project_has_tech). 22 tests.
**Shipped**: 2026-03-21. Total test count: 1246 → 1268. 20th detection category.

### N-68: State Management Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project state management pattern detection via `_find_state_management_patterns()` in connections.py. Analyzes state_management data from N-67 across the portfolio to detect: shared state management libraries (Redux/Zustand across 2+ projects, info), paradigm divergence (flux/store vs proxy-based vs atomic vs state machines vs Vue vs Angular paradigm families, warning), and state management gaps (frontend projects with React/Vue/Angular/etc. frameworks and 10+ source files but no state management library, warning). New connection types (`shared_state_mgmt`, `state_mgmt_divergence`, `state_mgmt_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps state_mgmt_gap and state_mgmt_divergence to `frontend` recommendation category. 20 categories in CONNECTION_CATEGORIES. 16 intelligence tests.
**Shipped**: 2026-03-21. Total test count: 1268 → 1284. Completes N-67 detection→intelligence pipeline.

### N-69: Doctor Category Summary
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: `atlas doctor` now shows a category breakdown line after the priority summary (e.g., "Categories: 3 security, 2 testing, 1 infra"). Groups recommendations by category and displays counts sorted by frequency (most common first). Helps users prioritize remediation by domain area rather than just severity. 3 tests.
**Shipped**: 2026-03-21. Total test count: 1284 → 1287. 20th experience feature.

### N-70: CSS & Styling Framework Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: `detect_css_frameworks()` in detector.py identifies CSS and styling frameworks from config files, file extensions, and package.json dependencies. Config files: tailwind.config.{js,ts,mjs,cjs}, postcss.config.*, .postcssrc*, stylelint.config.*, .stylelintrc*. File extensions: .scss/.sass (Sass), .less (Less), .module.css/.module.scss (CSS Modules) — checks root and src/. Package.json: Tailwind CSS, Styled Components, Emotion, Sass, Less, Stylus, PostCSS, Stylelint, Vanilla Extract, Linaria, Twin Macro, Stitches, Panda CSS, UnoCSS, Windi CSS, Bootstrap, Bulma, Chakra UI, Mantine, Material UI, Vuetify, Ant Design, Radix UI, shadcn/ui. Returns sorted deduplicated list. Integrated across models.py (TechStack field + to_dict/from_dict), scanner.py, display.py (project card + portfolio summary), export_report.py (CSV column + markdown detail + markdown summary + JSON summary), and cli.py (_project_has_tech). 29 tests.
**Shipped**: 2026-03-21. Total test count: 1287 → 1316. 21st detection category.

### N-71: CSS & Styling Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project CSS/styling pattern detection via `_find_css_framework_patterns()` in connections.py. Analyzes css_frameworks data from N-70 across the portfolio to detect: shared CSS frameworks (Tailwind/Bootstrap across 2+ projects, info), paradigm divergence (utility-first vs CSS-in-JS vs component library families, warning), and CSS gaps (frontend projects with React/Vue/Angular/etc. frameworks and 10+ source files but no CSS framework, warning). New connection types (`shared_css`, `css_divergence`, `css_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps css_gap and css_divergence to `frontend` recommendation category. 21 categories in CONNECTION_CATEGORIES. 14 intelligence tests.
**Shipped**: 2026-03-21. Total test count: 1316 → 1330. Completes N-70 detection→intelligence pipeline.

### N-72: Connection Category List Command
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: `atlas connections --type list` shows all available connection categories with their connection types. Displays category name, associated connection type names, and total category count. Updated help text from hardcoded category list to "use --type list to see all". Handles `list` as a special value before category lookup. Shows "21 categories available" footer. 4 tests.
**Shipped**: 2026-03-21. Total test count: 1330 → 1334. 21st experience feature.

### N-73: Bundler & Module Tool Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: `detect_bundlers()` in detector.py identifies JavaScript/TypeScript bundlers and module tools from config files and package.json dependencies. Config files: webpack.config.{js,ts,cjs,mjs}, vite.config.{js,ts,mjs}, rollup.config.{js,ts,mjs}, .parcelrc, turbo.json, .swcrc, rspack.config.{js,ts}, tsup.config.{ts,js}. Package.json: Webpack, Vite, esbuild, Rollup, Parcel, SWC, Turbopack, Rspack, tsup, unbuild, microbundle, Bun, Snowpack, WMR. Returns sorted deduplicated list. Integrated across models.py (TechStack field + to_dict/from_dict), scanner.py, display.py (project card + portfolio summary), export_report.py (CSV column + markdown detail + markdown summary + JSON summary), and cli.py (_project_has_tech). 24 tests.
**Shipped**: 2026-03-21. Total test count: 1334 → 1358. 22nd detection category.

### N-74: Bundler Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project bundler pattern detection via `_find_bundler_patterns()` in connections.py. Analyzes bundlers data from N-73 across the portfolio to detect: shared bundlers (Vite/Webpack across 2+ projects, info), generation divergence (modern/fast [Vite, esbuild, SWC, Turbopack, Rspack, Bun] vs traditional [Webpack, Rollup, Parcel, Snowpack] vs library [tsup, unbuild, microbundle], warning), and bundler gaps (JS/TS projects with 10+ source files but no bundler, warning). New connection types (`shared_bundler`, `bundler_divergence`, `bundler_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps bundler_gap and bundler_divergence to `frontend` recommendation category. 22 categories in CONNECTION_CATEGORIES. 12 intelligence tests.
**Shipped**: 2026-03-21. Total test count: 1358 → 1370. Completes N-73 detection→intelligence pipeline.

### N-75: Export Connection Summary Stats
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Markdown export now shows a connection summary line at the top of the Cross-Project Intelligence section (e.g., "**12 connections**: 3 warning, 9 info"). JSON export now includes a `connection_summary` object with `total`, `critical`, `warning`, and `info` counts alongside the full connections array. Gives consumers a quick overview of portfolio intelligence without parsing individual connections. 5 tests.
**Shipped**: 2026-03-21. Total test count: 1370 → 1375. 22nd experience feature.

### N-76: ORM & Database Client Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects ORM frameworks and database client libraries across all supported languages. Python: SQLAlchemy, SQLModel, Django ORM, Peewee, Tortoise ORM, Pony ORM, asyncpg, psycopg2/psycopg, PyMongo, Motor, MongoEngine, redis-py, aioredis, databases, Alembic. JavaScript/TypeScript: Prisma, TypeORM, Sequelize, Drizzle, Knex, Mongoose, Bookshelf, Objection.js, MikroORM, Kysely, better-sqlite3, node-postgres, ioredis, MongoDB Driver. Go: GORM, sqlx, ent, pgx, sqlc, Bun. Rust: Diesel, sqlx, SeaORM, Rusqlite. Java: Hibernate, MyBatis, jOOQ, Spring Data JPA, JDBI. Detects from config files (prisma/schema.prisma, ormconfig.*, drizzle.config.*, knexfile.*, mikro-orm.config.*), pyproject.toml, requirements.txt, package.json, go.mod, Cargo.toml, build.gradle, pom.xml. New TechStack field: orm_tools. 36 tests.
**Shipped**: 2026-03-21. Total test count: 1375 → 1411. 22nd detection feature.

### N-77: ORM Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project ORM and database client intelligence. Shared ORM detection (same tool in 2+ projects), ORM strategy divergence (ORM frameworks vs raw database clients — flags when portfolio mixes paradigms), ORM gap detection (projects with databases but no ORM/client library detected, min 10 source files). Connection types: shared_orm (info), orm_divergence (warning), orm_gap (warning). Added to CONNECTION_CATEGORIES as "orm" category (23rd). 11 tests.
**Shipped**: 2026-03-21. Total test count: 1411 → 1422. 24th intelligence feature.

### N-78: Connection Severity Filtering
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `--severity` / `-s` option on `atlas connections` command. Filters connections by severity level: info, warning, or critical. Shows filtered count summary. Invalid severity values show error with valid options. Combinable with `--type` for double filtering. 3 tests.
**Shipped**: 2026-03-21. Total test count: 1422 → 1425. 23rd experience feature.

### N-79: i18n & Localization Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects internationalization and localization tools across all supported languages. Directory detection: locales/, locale/, translations/, i18n/, lang/, messages/. Config files: lingui.config.*, .linguirc, babel.cfg, i18next-parser.config.*. JavaScript/TypeScript: i18next, react-i18next, next-i18next, next-intl, react-intl, FormatJS, vue-i18n, Angular i18n, Lingui, typesafe-i18n, rosetta, Polyglot, Globalize. Python: Babel, Flask-Babel, django-modeltranslation, django-rosetta, python-i18n. Go: go-i18n, golang.org/x/text. Rust: Fluent, rust-i18n. New TechStack field: i18n_tools. 26 tests.
**Shipped**: 2026-03-21. Total test count: 1425 → 1451. 23rd detection feature.

### N-80: i18n Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project i18n/localization intelligence. Shared i18n tool detection (same tool in 2+ projects), i18n strategy divergence (ICU/message format [react-intl, FormatJS] vs key-based [i18next, vue-i18n, next-intl] vs extraction-based [Lingui, Babel, Angular i18n]), i18n gap detection (web projects using React/Vue/Angular/Django/Flask/FastAPI/etc. with 10+ files but no i18n). Connection types: shared_i18n (info), i18n_divergence (warning), i18n_gap (warning). Added to CONNECTION_CATEGORIES as "i18n" category (24th). 10 tests.
**Shipped**: 2026-03-21. Total test count: 1451 → 1461. 25th intelligence feature.

### N-81: Project Search Command
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas search <term>` command for quick portfolio search. Matches against project name (substring), language (exact), framework (exact), and all tech fields via `_project_has_tech`. Results show health grade, health %, project name, and tech summary. Handles empty portfolios and no matches gracefully. 4 tests.
**Shipped**: 2026-03-21. Total test count: 1461 → 1465. 24th experience feature.

### N-82: Validation & Schema Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects validation and schema libraries across 5 ecosystems via `detect_validation_tools()` in detector.py. Python: Pydantic, marshmallow, Cerberus, attrs, cattrs, Voluptuous, schema, jsonschema, Colander, Schematics. JS/TS: Zod, Yup, Joi, class-validator, class-transformer, Ajv, Superstruct, Valibot, io-ts, TypeBox, Vest, myZod, Effect Schema, ArkType. Go: go-playground/validator, ozzo-validation. Rust: validator, garde. Java: Hibernate Validator, Jakarta Validation. Full pipeline: models.py field, scanner.py import/call, display.py project card + portfolio summary, export_report.py markdown/JSON/CSV, cli.py search integration. 30 tests.
**Shipped**: 2026-03-21. Total test count: 1465 → 1495. 24th detection feature.

### N-83: Validation Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project validation pattern detection via `_find_validation_patterns()` in connections.py. Analyzes validation_tools data from N-82 across the portfolio to detect: shared validation tools (Pydantic/Zod across 2+ projects, info), validation strategy divergence (schema-first vs model/decorator-based vs form validation, warning), and validation gaps (API/backend projects with 10+ source files using API frameworks but no validation library, critical). New connection types (`shared_validation`, `validation_divergence`, `validation_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps validation_gap and validation_divergence to `quality` recommendation category. 25th CONNECTION_CATEGORIES entry. 10 tests.
**Shipped**: 2026-03-21. Total test count: 1495 → 1505. 26th intelligence feature. Completes N-82 detection→intelligence pipeline.

### N-84: Batch Remove Stale Projects
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas batch-remove` command that prunes stale projects whose directories no longer exist on disk. Lists each stale project with name and path, removes them from portfolio, and saves. Handles empty portfolios and portfolios where all projects still exist gracefully. 4 tests.
**Shipped**: 2026-03-21. Total test count: 1505 → 1509. 25th experience feature.

### N-85: Logging Framework Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects logging and structured logging frameworks across 5 ecosystems via `detect_logging_tools()` in detector.py. Python: Loguru, structlog, python-json-logger, coloredlogs, Rich (logging), Logbook, Eliot, Twiggy. JS/TS: Winston, Pino, Bunyan, log4js, loglevel, Signale, Consola, Roarr, tslog, Winston Rotate, Morgan, debug. Go: Zap, Logrus, zerolog, slog. Rust: tracing, env_logger, log4rs, fern, slog. Java: Logback, Log4j, SLF4J. Full pipeline: models.py field, scanner.py import/call, display.py project card + portfolio summary, export_report.py markdown/JSON/CSV, cli.py search integration. 21 tests.
**Shipped**: 2026-03-21. Total test count: 1509 → 1530. 25th detection feature.

### N-86: Logging Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project logging pattern detection via `_find_logging_patterns()` in connections.py. Analyzes logging_tools data from N-85 across the portfolio to detect: shared logging tools (Loguru/Winston across 2+ projects, info), logging strategy divergence (structured logging like structlog/Pino/zerolog vs traditional logging like Winston/Log4j/Logrus, warning), and logging gaps (backend projects with 10+ source files using API frameworks but no logging framework, warning). New connection types (`shared_logging`, `logging_divergence`, `logging_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps logging_gap and logging_divergence to `infra` recommendation category. 26th CONNECTION_CATEGORIES entry. 10 tests.
**Shipped**: 2026-03-21. Total test count: 1530 → 1540. 27th intelligence feature. Completes N-85 detection→intelligence pipeline.

### N-87: Rename Project Command
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `atlas rename <old> <new>` command for renaming projects in the portfolio. Validates project exists, prevents name collisions with existing projects, persists the rename. 4 tests.
**Shipped**: 2026-03-21. Total test count: 1540 → 1544. 26th experience feature.

### N-88: Container Orchestration Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects container orchestration & IaC tools: Docker Compose, Kubernetes (k8s/kubernetes/kube/manifests/deploy dirs), Helm (Chart.yaml/charts dir), Kustomize, Skaffold, Tilt, Terraform, Pulumi, Ansible, Nomad, Docker Swarm, Vagrant, Packer. Added TechStack.container_orchestration field, wired through scanner, display, export, CLI search. 22 tests.
**Shipped**: 2026-03-21. Total test count: 1544 → 1566. 26th detection feature.

### N-89: Container Orchestration Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project container orchestration intelligence: shared orchestration tools (shared_container_orch), IaC vs Kubernetes-native vs Compose strategy divergence (container_orch_divergence), orchestration gaps for Docker projects (container_orch_gap). New CONNECTION_CATEGORIES entry "containers". 10 tests.
**Shipped**: 2026-03-21. Total test count: 1566 → 1575. 28th intelligence feature.

### N-90: Cloud Provider & SDK Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects cloud provider SDKs across Python (boto3, google-cloud-*, azure-*), JS/TS (@aws-sdk/*, @google-cloud/*, @azure/*), Go (aws-sdk-go, cloud.google.com/go), Rust (aws-sdk-*, google-cloud), Java (software.amazon.awssdk, com.google.cloud, com.azure). Also detects Cloudflare (wrangler), Fly.io, Railway, Render via config files. Added TechStack.cloud_providers field wired through scanner, display, export, CLI search. 22 tests.
**Shipped**: 2026-03-21. Total test count: 1575 → 1597. 27th detection feature.

### N-91: Cloud Provider Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project cloud provider intelligence: shared cloud providers (shared_cloud), hyperscaler vs edge/PaaS strategy divergence (cloud_divergence), multi-hyperscaler complexity warnings, cloud gaps for deployed projects (cloud_gap). New CONNECTION_CATEGORIES entry "cloud". 10 tests.
**Shipped**: 2026-03-21. Total test count: 1597 → 1606. 29th intelligence feature.

### N-92: Top Projects & Version Commands
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Two new CLI commands. `atlas top --by health|loc|tests|commits -n 5` shows top N projects ranked by metric with grade colors and tech summaries. `atlas version` shows installed package version. 5 tests.
**Shipped**: 2026-03-21. Total test count: 1606 → 1611. 27th experience feature.

### N-93: Task Queue & Background Job Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_task_queues()` in detector.py with refactored `_collect_python_deps()` helper. Detects task queues and background job frameworks across ecosystems: Python (Celery, RQ, Dramatiq, Huey, arq, TaskIQ, Temporal, Prefect, Airflow, Luigi, Dagster), JS/TS (BullMQ, Bull, Bee-Queue, Agenda, node-cron, Temporal, Graphile Worker, pg-boss, Quirrel), Go (Asynq, Temporal, robfig/cron, gocraft/work), Rust (tokio-cron-scheduler, Apalis), Java (Quartz, Spring Batch). Added `task_queues` field to TechStack model. Shows in `atlas inspect` project card, portfolio summary panel (display.py), markdown export project details and summary, JSON export portfolio_summary, and CSV export. `_project_has_tech()` searches task_queues. 19 detection tests.
**Shipped**: 2026-03-21. Total test count: 1611 → 1630. 28th detection category.

### N-94: Task Queue Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project task queue intelligence: shared task queues (shared_task_queue), traditional vs workflow vs cron paradigm divergence (task_queue_divergence), task queue gaps for backend projects without background jobs (task_queue_gap). New CONNECTION_CATEGORIES entry "queues". 10 tests.
**Shipped**: 2026-03-21. Total test count: 1630 → 1640. 30th intelligence feature.

### N-95: Export Filtering
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--grade`, `--lang`, `--has`, `--min-health`, `--max-health` filter options to `atlas export` command. Matches the same filter flags from `atlas status`. Works with all export formats (markdown, json, csv). Enables exporting targeted subsets of the portfolio. 5 tests.
**Shipped**: 2026-03-21. Total test count: 1640 → 1645. 28th experience feature.

### N-96: Search Engine Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_search_engines()` in detector.py. Detects search engines and full-text search tools across ecosystems: Python (Elasticsearch, OpenSearch, Meilisearch, Typesense, Algolia, Solr/pysolr, Whoosh, Haystack, Tantivy, Watson), JS/TS (Elasticsearch, OpenSearch, Meilisearch, Typesense, Algolia, Lunr, FlexSearch, Fuse.js, MiniSearch, Solr), Go (Elasticsearch, OpenSearch, Meilisearch, Typesense, Algolia, Bleve), Rust (Tantivy, Meilisearch, Elasticsearch), Java (Elasticsearch, OpenSearch, Solr, Algolia, Lucene). Added `search_engines` field to TechStack model. Shows in `atlas inspect` project card, portfolio summary panel, markdown/JSON/CSV export. `_project_has_tech()` searches search_engines. 20 detection tests.
**Shipped**: 2026-03-21. Total test count: 1645 → 1665. 29th detection category.

### N-97: Search Engine Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project search engine intelligence: shared search engines (shared_search), server-side vs client-side vs SaaS paradigm divergence (search_divergence), search gaps for database-backed projects (search_gap). New CONNECTION_CATEGORIES entry "search". 10 tests.
**Shipped**: 2026-03-21. Total test count: 1665 → 1675. 31st intelligence feature.

### N-98: Doctor JSON Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format json` option to `atlas doctor` command. Outputs structured JSON with total count, recommendations array (priority, category, message, projects), priority summary counts, and category breakdown. Enables CI pipeline integration and programmatic analysis of portfolio health recommendations. 3 tests.
**Shipped**: 2026-03-21. Total test count: 1675 → 1678. 29th experience feature.

### N-171: Doctor Result Limit
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--limit` / `-n` option to `atlas doctor` command. Limits the number of recommendations displayed. Applied after filters and sorting. Works with all output formats (rich, json, csv) and combines with --category, --priority, --project, and --sort. 3 tests.
**Shipped**: 2026-03-21. Total test count: 2430. 54th experience feature.

### N-170: Email Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project email and SMTP intelligence. Detects shared email libs (shared_email_lib — info) and SaaS/API-based vs SMTP/self-hosted paradigm divergence (email_lib_divergence — warning). SaaS: SendGrid, Mailgun, Postmark, Resend, Mailchimp, Mailjet, AWS SES, MJML, React Email. SMTP: Nodemailer, Flask-Mail, django-anymail, yagmail, Gomail, Lettre, JavaMail, Spring Mail. Companion to N-167. Added to CONNECTION_CATEGORIES (email), display type_labels/icons (✉), export type_labels, recommendations type_to_category. Capped at 10 connections. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2427. 54th intelligence feature.

### N-174: Export Result Limit
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--limit` / `-n` option to `atlas export` command. Limits the number of projects in export output. Applied after filters and sorting. Works with all output formats (markdown, json, csv) and combines with --grade, --lang, --has, --min-health, --max-health, and --sort. 3 tests.
**Shipped**: 2026-03-22. Total test count: 2460. 55th experience feature.

### N-175: Desktop & Cross-Platform Framework Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects desktop and cross-platform GUI frameworks. Python: PyQt5/6, PySide2/6, wxPython, Kivy, DearPyGui, CustomTkinter, Flet, PySimpleGUI, Toga, Textual, pyglet, Tkinter. JS/TS: Electron, Tauri, NW.js, Neutralino, Capacitor, React Native, Ionic. Go: Fyne, Wails, Gio. Rust: Iced, Dioxus, Slint, egui, druid, Tauri, gtk-rs. Java: JavaFX, Swing, SWT, Compose Desktop. Also detects tauri.conf.json and src-tauri directory. Added TechStack field `desktop_frameworks`, updated models/scanner/display/export. 24 tests.
**Shipped**: 2026-03-22. Total test count: 2484. 56th detection feature.

### N-176: A11y Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project accessibility tool intelligence. Detects shared a11y tools (shared_a11y_tool — info) and testing/auditing vs component/runtime paradigm divergence (a11y_divergence — warning). Testing: axe-core, Pa11y, Lighthouse, jest-axe, vitest-axe, cypress-axe, jsx-a11y, Testing Library. Component: React Aria, Radix UI, Reach UI, Downshift, react-focus-lock, focus-trap-react, ally.js, a11y-dialog, vue-a11y-utils. Companion to N-169. Added to CONNECTION_CATEGORIES (a11y), display type_labels/icons (♿), export type_labels, recommendations type_to_category. Capped at 10 connections. 7 tests.
**Shipped**: 2026-03-22. Total test count: 2491. 56th intelligence feature.

### N-177: Status Result Limit
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--limit` / `-n` option to `atlas status` command. Limits the number of projects displayed. Applied after sorting. Works with all output formats (rich, json, csv) and combines with --grade, --lang, --has, --min-health, --max-health, --sort, and --grades. 3 tests.
**Shipped**: 2026-03-22. Total test count: 2494. 56th experience feature.

### N-178: Scraping Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project scraping library intelligence. Companion to N-172 (detection). Detects shared scraping libs (shared_scraping_lib — info) and browser-based vs parser-based paradigm divergence (scraping_lib_divergence — warning). Browser: Puppeteer, Playwright, Crawlee, chromedp, rod, headless_chrome. Parser: BeautifulSoup, lxml, Cheerio, jsdom, goquery, scraper, jsoup, Parsel. Added CONNECTION_CATEGORIES (scraping), display icons (🕷), export/display type_labels, recommendations mapping. Capped at 10. 7 tests.
**Shipped**: 2026-03-22. Total test count: 2501.

### N-179: Desktop Framework Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project desktop framework intelligence. Companion to N-175 (detection). Detects shared desktop frameworks (shared_desktop_framework — info) and native toolkit vs web-wrapped paradigm divergence (desktop_framework_divergence — warning). Native: PyQt5/6, PySide2/6, wxPython, Kivy, Swing, JavaFX, Fyne, Iced, egui, gtk-rs. Web-wrapped: Electron, Tauri, NW.js, Neutralino, Wails, Capacitor, Ionic, Flet. Added CONNECTION_CATEGORIES (desktop), display icons (🖥), export/display type_labels, recommendations mapping. Capped at 10. 7 tests.
**Shipped**: 2026-03-22. Total test count: 2508.

### N-180: File Storage & Object Store Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for file storage and object store libraries. Detection: Python (boto3, aioboto3, s3fs, google-cloud-storage, gcsfs, azure-storage-blob, minio, cloudinary, django-storages, flask-uploads, python-magic, smart-open), JS/TS (@aws-sdk/client-s3, aws-sdk, @google-cloud/storage, @azure/storage-blob, minio, cloudinary, uploadthing, @vercel/blob, @supabase/storage-js, multer, formidable, busboy, @cloudflare/r2, firebase/storage), Go (aws-sdk-go, cloud.google.com/go/storage, azure-storage-blob-go, minio/minio-go), Rust (aws-sdk-s3, rusoto_s3, cloud-storage, object_store), Java (aws+s3, google-cloud-storage, azure-storage-blob, minio). Intelligence: shared_file_storage (info), file_storage_divergence cloud-native (AWS S3, GCS, Azure Blob, MinIO) vs dev-platform (UploadThing, Vercel Blob, Supabase Storage, Cloudinary) (warning). TechStack field `file_storage`, CONNECTION_CATEGORIES (storage), display icons (📦), export/display type_labels, recommendations mapping. Capped at 10. 19 detection tests + 7 intelligence tests = 26 tests.
**Shipped**: 2026-03-22. Total test count: 2534.

### N-181: Form Library Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for form libraries. Detection: Python (wtforms, flask-wtf, django-crispy-forms, django-formtools), JS/TS (react-hook-form, formik, final-form, @tanstack/react-form, conform-to, react-jsonschema-form, uniforms, vee-validate, formkit, vuelidate, react-aria, angular/forms, svelte-forms-lib, felte, sveltekit-superforms). Intelligence: shared_form_lib (info), form_lib_divergence schema-driven (React Hook Form, VeeValidate, Conform, TanStack Form) vs imperative (Formik, Final Form, Uniforms, WTForms) (warning). TechStack field `form_libs`, CONNECTION_CATEGORIES (forms), display icons (📝), export/display type_labels, recommendations mapping. Capped at 10. 14 detection tests + 7 intelligence tests = 21 tests.
**Shipped**: 2026-03-22. Total test count: 2556.

### N-182: Animation Library Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for animation and motion libraries. Detection: Python (Manim, pyglet, Arcade), JS/TS (Framer Motion, GSAP, anime.js, Lottie, react-spring, Motion One, AutoAnimate, Rive, Popmotion, Theatre.js, Velocity.js, VueUse Motion, AnimXYZ, React Transition Group, Svelte Motion, Vue Kinesis), Rust (keyframe, interpolation). Intelligence: shared_animation_lib (info), animation_lib_divergence declarative (Framer Motion, react-spring, AutoAnimate, Motion One) vs imperative (GSAP, anime.js, Velocity.js, Lottie) (warning). TechStack field `animation_libs`, CONNECTION_CATEGORIES (animation), display icons (🎬), export/display type_labels, recommendations mapping. Capped at 10. 20 detection tests + 7 intelligence tests = 27 tests.
**Shipped**: 2026-03-22. Total test count: 2583.

### N-183: Routing Library Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for URL routing and navigation libraries. Detection: Python (Flask Routes, FastAPI Router, Django URLs, Starlette/aiohttp/Sanic/Falcon/Bottle Routes), JS/TS (React Router, TanStack Router, Vue Router, Angular Router, Wouter, SvelteKit Router, Expo Router, React Navigation, Navigo, Reach Router), Go (Gorilla Mux, Chi, Gin/Echo/Fiber Router, httprouter), Rust (Axum/Actix Web/Warp/Rocket Router), Java (Spring MVC/WebFlux Router, Javalin, Spark Java). Intelligence: shared_routing_lib (info), routing_lib_divergence framework-integrated (React Router, Vue Router, Django URLs) vs standalone (TanStack Router, Wouter, Chi) (warning). TechStack field `routing_libs`, CONNECTION_CATEGORIES (routing), display icons (🔀), export/display type_labels, recommendations mapping. Capped at 10. 18 detection tests + 7 intelligence tests = 25 tests.
**Shipped**: 2026-03-22. Total test count: 2608.

### N-184: Game Development Framework Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for game development frameworks. Detection: Python (Pygame, Arcade, pyglet, Panda3D, Ursina, Pyxel, Cocos2d, Ren'Py), JS/TS (Phaser, PixiJS, Three.js, Babylon.js, Kaboom.js, Excalibur, melonJS, PlayCanvas, A-Frame, Matter.js, Cannon.js, Planck.js, GDevelop), Go (Ebiten, Pixel, g3n, Go GL), Rust (Bevy, ggez, macroquad, Piston, Amethyst, Fyrox, Tetra), Java (LibGDX, LWJGL, jMonkeyEngine, Slick2D). Intelligence: shared_game_framework (info), game_framework_divergence 2D (Pygame, Phaser, PixiJS) vs 3D (Three.js, Babylon.js, Bevy) (warning). TechStack field `game_frameworks`, CONNECTION_CATEGORIES (games), display icons (🎮), export/display type_labels, recommendations mapping. Capped at 10. 18 detection tests + 7 intelligence tests = 25 tests.
**Shipped**: 2026-03-22. Total test count: 2633.

### N-185: CMS & Headless CMS Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for CMS and headless CMS tools. Detection: Python (Wagtail, django CMS, Mezzanine, Pelican, Lektor, MkDocs, Nikola), JS/TS (Strapi, Sanity, Contentful, Ghost, KeystoneJS, Payload CMS, Directus, TinaCMS, Contentlayer, Nextra, Builder.io, Storyblok, Prismic, WordPress, Decap CMS, Hygraph), Go/config (Hugo — via hugo.toml/yaml/json/config.toml), Ruby (Jekyll — via _config.yml + Gemfile). Intelligence: shared_cms (info), cms_divergence headless (Strapi, Sanity, Contentful) vs traditional (WordPress, Wagtail, Hugo) (warning). TechStack field `cms_tools`, CONNECTION_CATEGORIES (cms), display icons (📰), export/display type_labels, recommendations mapping. Capped at 10. 16 detection tests + 7 intelligence tests = 23 tests.
**Shipped**: 2026-03-22. Total test count: 2656.

### N-186: Rate Limiting Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for rate limiting libraries. Detection: Python (SlowAPI, Flask-Limiter, django-ratelimit, django-axes, Limits, aiolimiter, fastapi-limiter, Token Bucket), JS/TS (express-rate-limit, rate-limiter-flexible, NestJS Throttler, Bottleneck, p-throttle, Upstash Ratelimit, express-slow-down), Go (Tollbooth, go-limiter, juju/ratelimit, x/time/rate), Rust (Governor, actix-limitation, tower-rate-limit), Java (Bucket4j, Resilience4j, Guava RateLimiter). Intelligence: shared_rate_limiter (info), rate_limiter_divergence middleware (express-rate-limit, SlowAPI) vs library (Bottleneck, rate-limiter-flexible, Governor) (warning). TechStack field `rate_limiters`, CONNECTION_CATEGORIES (rate-limiting), display icons (🚦), export/display type_labels, recommendations mapping. Capped at 10. 14 detection tests + 7 intelligence tests = 21 tests.
**Shipped**: 2026-03-22. Total test count: 2677.

### N-187: Database Migration Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for database migration tools. Detection: Python (Alembic, Django Migrations, Yoyo, Aerich, Piccolo Migrations), JS/TS (Prisma Migrate, Drizzle Kit, Knex/TypeORM/Sequelize/MikroORM/Kysely Migrations, db-migrate, Umzug, node-pg-migrate), Go (golang-migrate, Goose, sql-migrate, dbmate, Atlas), Rust (Diesel/SeaORM/sqlx Migrations, Refinery, Barrel), Java (Flyway, Liquibase, MyBatis Migrations). Intelligence: shared_db_migration (info), db_migration_divergence ORM-integrated (Alembic, Prisma Migrate, Django Migrations) vs standalone (Flyway, golang-migrate, Goose) (warning). TechStack field `db_migration_tools`, CONNECTION_CATEGORIES (migrations), display icons (🔄), export/display type_labels, recommendations mapping. Capped at 10. 15 detection tests + 7 intelligence tests = 22 tests.
**Shipped**: 2026-03-22. Total test count: 2699.

### N-188: gRPC & RPC Framework Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for gRPC and RPC framework libraries. Detection: Python (gRPC, betterproto, Apache Thrift, RPyC, Pyro5, Pyro4, zerorpc, JSON-RPC), JS/TS (gRPC, tRPC, ConnectRPC, JSON-RPC, nice-grpc, Mali), Go (gRPC, ConnectRPC, Twirp, Apache Thrift, rpcx), Rust (Tonic, tarpc, Cap'n Proto, Prost), Java (gRPC, Apache Dubbo, Apache Avro RPC), Protobuf (.proto files). Intelligence: shared_grpc_lib (info), grpc_divergence schema-based (gRPC, tRPC, ConnectRPC, Protobuf) vs dynamic (JSON-RPC, RPyC, zerorpc) (warning). TechStack field `grpc_libs`, CONNECTION_CATEGORIES (grpc), display icons (📡), export/display type_labels, recommendations mapping. Capped at 10. 17 detection tests + 7 intelligence tests = 24 tests.
**Shipped**: 2026-03-22. Total test count: 2723.

### N-189: Code Generation Tool Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for code generation tools. Detection: Python (protoc, datamodel-code-generator, Cookiecutter, Copier, OpenAPI Generator, betterproto Codegen, pydantic-to-typescript), JS/TS (GraphQL Codegen, OpenAPI Generator, openapi-typescript, swagger-typescript-api, ts-proto, Buf, quicktype, json-schema-to-typescript, Prisma Generate, Plop, Hygen), Go (sqlc, gqlgen, oapi-codegen, Ent, Buf), Rust (Prost Build, Tonic Build, bindgen, cbindgen), Java (protoc, OpenAPI Generator, Swagger Codegen, MapStruct, Lombok, jOOQ Codegen, Immutables), Buf config (buf.yaml/buf.gen.yaml). Intelligence: shared_codegen_tool (info), codegen_divergence schema-driven (protoc, GraphQL Codegen, OpenAPI Generator, sqlc) vs template-driven (Plop, Hygen, Cookiecutter, Lombok) (warning). TechStack field `codegen_tools`, CONNECTION_CATEGORIES (codegen), display icons (⚙️), export/display type_labels, recommendations mapping. Capped at 10. 20 detection tests + 7 intelligence tests = 27 tests.
**Shipped**: 2026-03-22. Total test count: 2750.

### N-190: Mocking & Test Fixture Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for mocking and test fixture libraries. Detection: Python (pytest-mock, responses, HTTPretty, VCR.py, requests-mock, RESPX, aioresponses, FreezeGun, time-machine, Faker, Factory Boy, Model Bakery, Hypothesis, Moto, LocalStack), JS/TS (MSW, nock, Sinon.js, Faker.js, Fishery, Mirage JS, Polly.js, jest-mock-extended, JSON Server), Go (testify, gomock, httpmock, gock, GoFakeIt), Rust (mockall, mockito-rs, wiremock-rs, fake-rs, proptest, httpmock-rs), Java (Mockito, WireMock, PowerMock, EasyMock, JavaFaker, DataFaker, Testcontainers). Intelligence: shared_mocking_lib (info), mocking_divergence HTTP/service (MSW, nock, responses, WireMock) vs unit/object (pytest-mock, Sinon.js, Mockito, gomock) (warning). TechStack field `mocking_libs`, CONNECTION_CATEGORIES (mocking), display icons (🎭), export/display type_labels, recommendations mapping. Capped at 10. 18 detection tests + 7 intelligence tests = 25 tests.
**Shipped**: 2026-03-22. Total test count: 2775.

### N-191: Changelog & Release Tool Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for changelog and release tools. Detection: Python (bump2version, bumpversion, python-semantic-release, Towncrier, Commitizen, Versioneer, setuptools-scm, PBR, Incremental), JS/TS (semantic-release, standard-version, Changesets, release-it, conventional-changelog, auto, np, Lerna, release-please, bumpp), Go (GoReleaser — via .goreleaser.yml), Rust (cargo-release, cargo-dist), Java (Maven Release Plugin, Axion Release Plugin), config files (.releaserc, .changeset dir, cliff.toml, .release-it.json, CHANGELOG.md). Intelligence: shared_release_tool (info), release_tool_divergence automated (semantic-release, Changesets, release-please) vs manual (standard-version, np, bump2version) (warning). TechStack field `release_tools`, CONNECTION_CATEGORIES (releases), display icons (🏷️), export/display type_labels, recommendations mapping. Capped at 10. 15 detection tests + 7 intelligence tests = 22 tests.
**Shipped**: 2026-03-22. Total test count: 2798.

### N-192: E2E & Browser Testing Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for E2E and browser testing tools. Detection: Python (Selenium, Playwright, Splinter, Pyppeteer, Helium, Robot Framework, Behave, pytest-bdd, Locust, Appium), JS/TS (Cypress, Playwright, WebdriverIO, Puppeteer, TestCafe, Nightwatch, Detox, CodeceptJS, Selenium, Appium, Protractor), Go (chromedp, Rod, Selenium), Rust (thirtyfour, fantoccini, headless_chrome), Java (Selenium, Selenide, Cucumber, Karate, REST Assured, Appium), config files (cypress.config.ts/js, playwright.config.ts/js). Intelligence: shared_e2e_tool (info), e2e_divergence modern (Cypress, Playwright, TestCafe) vs traditional (Selenium, WebdriverIO, Puppeteer) (warning). TechStack field `e2e_testing`, CONNECTION_CATEGORIES (e2e), display icons (🌐), export/display type_labels, recommendations mapping. Capped at 10. 16 detection tests + 7 intelligence tests = 23 tests.
**Shipped**: 2026-03-22. Total test count: 2821.

### N-193: Monorepo Tool Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for monorepo tools. Detection: JS/TS (Nx, Turborepo, Lerna, Changesets, Rush, Moon, Wireit, ultra-runner, pnpm Workspaces), config files (nx.json, turbo.json, lerna.json, rush.json, pnpm-workspace.yaml), build systems (Bazel, Pants, Buck2), Go (go.work — Go Workspaces), Rust ([workspace] in Cargo.toml — Cargo Workspaces). Intelligence: shared_monorepo_tool (info), monorepo_divergence JS-native (Nx, Turborepo, Lerna, Rush, Moon) vs polyglot (Bazel, Pants, Buck2) (warning). TechStack field `monorepo_tools`, CONNECTION_CATEGORIES (monorepo), display icons (📦), export/display type_labels, recommendations mapping. Capped at 10. 14 detection tests + 7 intelligence tests = 21 tests.
**Shipped**: 2026-03-22. Total test count: 2842.

### N-194: Error Tracking & APM Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for error tracking and APM tools. Detection: Python (Sentry, Datadog APM, New Relic, Elastic APM, OpenTelemetry, Rollbar, Bugsnag, Honeybadger, Airbrake, Pyroscope), JS/TS (Sentry, Datadog, New Relic, Elastic APM, OpenTelemetry, Rollbar, Bugsnag, Honeybadger, Airbrake, LogRocket, Highlight, AppSignal), Go (Sentry, Datadog, New Relic, Elastic APM, OpenTelemetry, Rollbar, Bugsnag, Honeybadger), Rust (Sentry, OpenTelemetry), Java (Sentry, Datadog, New Relic, Elastic APM, OpenTelemetry, Rollbar, Bugsnag, Honeybadger). Intelligence: shared_error_tracker (info), error_tracking_divergence hosted (Sentry, Rollbar, Bugsnag) vs agent-based (Datadog APM, New Relic, Elastic APM) (warning). TechStack field `error_tracking`, CONNECTION_CATEGORIES (errors), display icons (🚨), export/display type_labels, recommendations mapping. Capped at 10. 17 detection tests + 7 intelligence tests = 24 tests.
**Shipped**: 2026-03-22. Total test count: 2866.

### N-195: Static Site Generator Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for static site generators and JAMstack frameworks. Detection: Python (MkDocs, Sphinx, Pelican, Nikola, Lektor), JS/TS (Next.js, Gatsby, Astro, Nuxt, SvelteKit, Eleventy, VitePress, VuePress, Docusaurus, Remix, Hexo, Gridsome), Go (Hugo), Ruby (Jekyll, Middleman, Bridgetown), config files (hugo.toml, _config.yml, mkdocs.yml, conf.py, astro.config.mjs, next.config.js, nuxt.config.ts, docusaurus.config.js, .eleventy.js). Intelligence: shared_ssg (info), ssg_divergence app-framework (Next.js, Gatsby, Astro) vs docs-focused (MkDocs, Sphinx, Docusaurus) (warning). TechStack field `static_site_generators`, CONNECTION_CATEGORIES (ssg), display icons (🏗️), export/display type_labels, recommendations mapping. Capped at 10. 16 detection tests + 7 intelligence tests = 23 tests.
**Shipped**: 2026-03-22. Total test count: 2889.

### N-196: Analytics & Product Analytics Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for analytics and product analytics tools. Detection: Python (PostHog, Mixpanel, Amplitude, Segment, Plausible, RudderStack, Countly), JS/TS (PostHog, Mixpanel, Amplitude, Segment, Plausible, Google Analytics, Heap, RudderStack, FullStory, Hotjar, Pirsch, Umami, Vercel Analytics), Go (PostHog, Mixpanel, Amplitude, Segment), Java (PostHog, Mixpanel, Amplitude, Segment). Intelligence: shared_analytics_tool (info), analytics_divergence privacy-first (PostHog, Plausible, Umami) vs commercial (Mixpanel, Amplitude, Google Analytics) (warning). TechStack field `analytics_tools`, CONNECTION_CATEGORIES (analytics), display icons (📊), export/display type_labels, recommendations mapping. Capped at 10. 15 detection tests + 7 intelligence tests = 22 tests.
**Shipped**: 2026-03-22. Total test count: 2911.

### N-197: Mobile Framework Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for mobile development frameworks. Detection: JS/TS (React Native, Expo, Ionic, Capacitor, NativeScript, Tauri, Quasar), Dart (Flutter), Kotlin (Kotlin Multiplatform), Java (Android Native), Swift (Swift Package, Xcode), .NET (MAUI, Xamarin), config files (app.json, capacitor.config, ionic.config.json, tauri.conf.json, pubspec.yaml). Intelligence: shared_mobile_framework (info), mobile_divergence cross-platform JS (React Native, Ionic, Capacitor) vs native/cross-native (Flutter, Kotlin Multiplatform, .NET MAUI) (warning). TechStack field `mobile_frameworks`, CONNECTION_CATEGORIES (mobile), display icons (📱), export/display type_labels, recommendations mapping. Capped at 10. 14 detection tests + 7 intelligence tests = 21 tests.
**Shipped**: 2026-03-22. Total test count: 2932.

### N-198: Workflow Engine Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for workflow and orchestration engines. Detection: Python (Airflow, Prefect, Dagster, Temporal, Luigi, Mage, Apache Beam, dbt, Kedro, Flyte, APScheduler, Dramatiq, Huey), JS/TS (BullMQ, node-cron, Agenda, Bee Queue, Temporal, Inngest, Trigger.dev, n8n), Go (Temporal, Cadence, Asynq, Machinery), Java (Temporal, Camunda, Apache Camel, Quartz, Spring Batch, Activiti), config dirs (dags/, dbt_project.yml, prefect.yaml). Intelligence: shared_workflow_engine (info), workflow_divergence pipeline (Airflow, Dagster, dbt) vs task-oriented (Temporal, BullMQ, Dramatiq) (warning). TechStack field `workflow_engines`, CONNECTION_CATEGORIES (workflows), display icons (⚙️), export/display type_labels, recommendations mapping. Capped at 10. 16 detection tests + 7 intelligence tests = 23 tests.
**Shipped**: 2026-03-23. Total test count: 2979.

### N-199: Secrets Management Detection + Intelligence
**Pillar**: DETECTION+INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Bundled detection + intelligence for secrets management. Detection: Python (dotenv, HashiCorp Vault/hvac, Pydantic Settings, python-decouple, Environs), JS/TS (dotenv, HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault, Infisical, Doppler, env-cmd, T3 Env), Go (HashiCorp Vault, dotenv, Viper), Rust (dotenv), Java (HashiCorp Vault, Jasypt), config files (.env, .env.example, .sops.yaml, vault.hcl, .infisical.json, doppler.yaml). Intelligence: shared_secrets_tool (info), secrets_divergence env-file (dotenv, python-decouple, Viper) vs managed (HashiCorp Vault, AWS Secrets Manager, Doppler) (warning). TechStack field `secrets_management`, CONNECTION_CATEGORIES (secrets), display icons (🔐), export/display type_labels, recommendations mapping. Capped at 10. 17 detection tests + 7 intelligence tests = 24 tests.
**Shipped**: 2026-03-23. Total test count: 2979.

### N-173: Compression Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project compression and archive intelligence. Detects shared compression libs (shared_compression_lib — info) and archival vs streaming paradigm divergence (compression_lib_divergence — warning). Archival: JSZip, archiver, tar-stream, 7-Zip, RAR, Commons Compress. Streaming: LZ4, Snappy, Zstandard, Brotli, Blosc, pako, fflate, klauspost/compress. Companion to N-163. Added to CONNECTION_CATEGORIES (compression), display type_labels/icons (🗜), export type_labels, recommendations type_to_category. Capped at 10 connections. 7 tests.
**Shipped**: 2026-03-22. Total test count: 2457. 55th intelligence feature.

### N-172: Web Scraping & Crawling Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects web scraping and crawling libraries across Python (Scrapy, BeautifulSoup, lxml, Parsel, MechanicalSoup, requests-html, selectolax, gazpacho, newspaper3k, trafilatura, cssselect, pyquery, html5lib), JS/TS (Puppeteer, Playwright, Cheerio, Crawlee, x-ray, jsdom, node-html-parser, linkedom, happy-dom), Go (Colly, goquery, chromedp, rod), Rust (scraper, select.rs, spider, headless_chrome), Java (jsoup, HtmlUnit, WebMagic, crawler4j, Apache Nutch). TechStack field `scraping_libs`, portfolio summary, project card, CSV/MD/JSON export. 20 tests.
**Shipped**: 2026-03-22. Total test count: 2450. 55th detection category.

### N-169: Accessibility & A11y Tool Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects accessibility and a11y testing/linting tools across Python (axe-selenium-python, Playwright, Selenium, Pa11y) and JS/TS (axe-core, jsx-a11y, React Aria, Radix UI, Reach UI, Downshift, react-focus-lock, focus-trap-react, Pa11y, Lighthouse, Testing Library, jest-axe, vitest-axe, cypress-axe, ally.js, a11y-dialog, vue-a11y-utils). Also detects .accessibilityrc and .pa11yci config files. TechStack field `a11y_tools`, portfolio summary, project card, CSV/MD/JSON export. 19 tests.
**Shipped**: 2026-03-21. Total test count: 2420. 54th detection category.

### N-168: Connections Result Limit
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--limit` / `-n` option to `atlas connections` command. Limits the number of connections displayed. Applied after filters and sorting. Works with all output formats (rich, json, csv), --summary, and all existing filters (--type, --severity, --project). 3 tests.
**Shipped**: 2026-03-21. Total test count: 2401. 53rd experience feature.

### N-167: Email & SMTP Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects email and SMTP libraries across Python (SendGrid, Mailgun, Postmark, Resend, django-anymail, Flask-Mail, django-ses, yagmail, redmail, aiosmtplib, Mailchimp, Mailjet), JS/TS (Nodemailer, SendGrid, Resend, Postmark, Mailchimp, Mailgun, AWS SES, MJML, React Email, Plunk), Go (Gomail, jordan-wright/email, go-smtp, SendGrid, Mailgun), Rust (Lettre, mail-send, SendGrid), Java (JavaMail, Jakarta Mail, Spring Mail, Commons Email, SendGrid, Simple Java Mail). TechStack field, portfolio summary, project card, CSV/MD/JSON export. 18 tests.
**Shipped**: 2026-03-21. Total test count: 2391 → 2398. 53rd detection category.

### N-166: PDF & Document Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project PDF and document intelligence. Detects shared PDF/doc libs (shared_pdf_lib — info) and generation vs extraction paradigm divergence (pdf_lib_divergence — warning). Generation: ReportLab, WeasyPrint, FPDF2, python-docx, openpyxl, XlsxWriter, jsPDF, pdfmake, pdf-lib, iText, printpdf. Extraction: pypdf, pdfplumber, PyMuPDF, PDFMiner, Camelot, tabula-py, SheetJS, PDF.js, Apache PDFBox. Companion to N-146. Added to CONNECTION_CATEGORIES (pdf), display type_labels/icons, export type_labels, recommendations type_to_category. Capped at 10 connections. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2380 → 2387. 53rd intelligence feature.

### N-165: Search Result Limit
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--limit` / `-n` option to `atlas search` command. Limits the number of results displayed. Applied after sorting, so `--sort health --limit 3` shows the 3 healthiest matches. Works with all output formats (rich, json) and combines with --sort. 3 tests.
**Shipped**: 2026-03-21. Total test count: 2373. 52nd experience feature.

### N-164: Cryptography Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project cryptography intelligence. Detects shared crypto libs (shared_crypto_lib — info) and high-level vs low-level paradigm divergence (crypto_lib_divergence — warning). High-level: bcrypt, Passlib, Argon2, Tink, jose, PyNaCl, libsodium, TweetNaCl, OpenPGP.js, noble-curves, age. Low-level: cryptography, PyCryptodome, pyOpenSSL, CryptoJS, node-forge, ring, rustls, sha2, aes-gcm, x/crypto. Added to CONNECTION_CATEGORIES (crypto), display type_labels/icons, export type_labels, recommendations type_to_category. Capped at 10 connections. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2363 → 2370. 52nd intelligence feature.

### N-163: Compression & Archive Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects compression and archive libraries across Python (Zstandard, LZ4, Brotli, Snappy, Blosc, Blosc2, 7-Zip, RAR, patool, pyunpack), JS/TS (pako, fflate, JSZip, archiver, compressing, tar-stream, yazl, yauzl, adm-zip, LZ4, Snappy, Brotli, Zstandard), Go (klauspost/compress, pgzip, LZ4, Zstandard, archiver, xz), Rust (flate2, LZ4, Zstandard, Brotli, Snappy, xz), Java (Commons Compress, Snappy, LZ4, Zstandard, Brotli, Zip4j, JUnrar). TechStack field, portfolio summary, project card, CSV/MD/JSON export. 19 tests.
**Shipped**: 2026-03-21. Total test count: 2344 → 2363. 52nd detection category.

### N-162: Doctor Project Filter
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--project` option to `atlas doctor` command. Filters recommendations to only those involving a specific project. `--project myapp` shows only recommendations that mention "myapp" in their projects list. Works with all output formats (rich, json, csv) and combines with --category and --priority filters. Shows "No recommendations" when project not found. 3 tests.
**Shipped**: 2026-03-21. Total test count: 2344. 51st experience feature.

### N-161: Async Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project async/concurrency intelligence. Detects shared async libs (shared_async_lib — info) and reactive vs parallel paradigm divergence (async_lib_divergence — warning). Reactive: Twisted, trio, AnyIO, Tokio, async-std, RxJS, RxJava, Project Reactor, Akka, Vert.x. Parallel: Celery, Rayon, Crossbeam, workerpool, Piscina, Tinypool, multiprocessing, concurrent.futures. Added to CONNECTION_CATEGORIES (async), display type_labels/icons, export type_labels, recommendations type_to_category. Capped at 10 connections. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2334 → 2341. 51st intelligence feature.

### N-160: Concurrency & Async Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects concurrency and async libraries across Python (Twisted, trio, AnyIO, Gevent, uvloop, Curio, Greenlet, Celery, multiprocessing, concurrent.futures, aiofiles, aiomultiprocess), JS/TS (RxJS, p-queue, p-limit, async, Bluebird, workerpool, threads.js, Comlink, Piscina, Tinypool, observable-fns), Go (x/sync, conc, ants, pond), Rust (Tokio, async-std, smol, Rayon, Crossbeam, futures, flume), Java (RxJava, Project Reactor, Akka, Vert.x, Quasar, Kotlin Coroutines). TechStack field, portfolio summary, project card, CSV/MD/JSON export, CLI search. 19 tests.
**Shipped**: 2026-03-21. Total test count: 2315 → 2334. 51st detection category.

### N-159: Top Projects Filter
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--lang` and `--has` filter options to `atlas top` command. Filters projects before ranking by metric. `--lang Python` shows only Python projects. `--has Docker` shows only projects with Docker. Works with all metrics (health, loc, tests, commits), output formats (rich, json, csv), and --limit. Shows "No projects match" when filters exclude everything. 3 tests.
**Shipped**: 2026-03-21. Total test count: 2315. 50th experience feature.

### N-158: Math Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project math/scientific computing intelligence. Detects shared math libs (shared_math_lib — info) and numerical vs statistical paradigm divergence (math_lib_divergence — warning). Numerical: NumPy, SciPy, Numba, CuPy, JAX, Dask, Gonum, nalgebra, etc. Statistical: scikit-learn, statsmodels, PyMC, Linfa, Smile, etc. Added to CONNECTION_CATEGORIES (math), display type_labels/icons, export type_labels, recommendations type_to_category. Capped at 10 connections. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2305 → 2312. 50th intelligence feature.

### N-157: Math & Scientific Computing Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects math and scientific computing libraries across Python (NumPy, SciPy, SymPy, Pandas, Polars, scikit-learn, Numba, Dask, Modin, Vaex, CuPy, JAX, PyMC, ArviZ, CVXPY, statsmodels, NetworkX), JS/TS (math.js, Numeric.js, ML-Matrix, simple-statistics, jStat, stdlib, ndarray, TensorFlow.js, Danfo.js, Arquero), Go (Gonum, stats, sparse), Rust (nalgebra, ndarray, statrs, peroxide, Linfa), Java (Commons Math, EJML, ND4J, Tablesaw, Smile). TechStack field, portfolio summary, project card, CSV/MD/JSON export, CLI search. 18 tests.
**Shipped**: 2026-03-21. Total test count: 2287 → 2305. 50th detection category.

### N-156: Export Sort Command
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--sort` option to `atlas export` command. Supports sorting by name (alphabetical), health (descending), and loc (descending). Works with all export formats (markdown, json, csv) and all existing filters. 3 tests.
**Shipped**: 2026-03-21. Total test count: 2284 → 2287. 49th experience feature.

### N-155: Media Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project media library intelligence. Detects shared media libs (shared_media_lib — info) and audio vs video paradigm divergence (media_lib_divergence — warning). Audio: Pydub, Librosa, SoundFile, PyAudio, torchaudio, Tone.js, Howler.js, Rodio, etc. Video: MoviePy, PyAV, Video.js, HLS.js, Shaka Player, Mediasoup, JavaCV, etc. Added to CONNECTION_CATEGORIES (media), display type_labels/icons, export type_labels, recommendations type_to_category. Capped at 10 connections. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2277 → 2284. 49th intelligence feature.

### N-154: Audio/Video & Media Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects audio/video and media processing libraries across Python (FFmpeg, MoviePy, Pydub, Librosa, SoundFile, PyAudio, PyAV, torchaudio, Decord, VidGear, aubio, madmom, Essentia, music21, Pedalboard, sounddevice, audioread), JS/TS (fluent-ffmpeg, Tone.js, Howler.js, WaveSurfer.js, Video.js, Plyr, HLS.js, DASH.js, Shaka Player, Mediasoup, SimplePeer, PeerJS, FFmpeg.wasm, music-metadata), Go (Beep, Oto, Ebiten, go-dash, GoAV), Rust (Rodio, CPAL, Symphonia, GStreamer, FFmpeg, dasp), Java (JavaCV, JCodec, Xuggler, JAVE, TarsosDSP, Tritonus, JLayer). TechStack field, portfolio summary, project card, CSV/MD/JSON export, CLI search. 19 tests.
**Shipped**: 2026-03-21. Total test count: 2258 → 2277. 49th detection category.

### N-153: Search Sort Command
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--sort` option to `atlas search` command. Supports sorting by name (alphabetical), health (descending), and loc (descending). Works with JSON output format. 3 tests.
**Shipped**: 2026-03-21. Total test count: 2255 → 2258. 48th experience feature.

### N-152: Geospatial Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project geospatial intelligence. Detects shared geo libs (shared_geo_lib — info) and mapping vs analysis paradigm divergence (geo_lib_divergence — warning). Mapping: Leaflet, Mapbox GL, MapLibre GL, OpenLayers, Cesium, Google Maps, etc. Analysis: GeoPandas, Shapely, Fiona, rasterio, GDAL, Turf.js, GeoTools, JTS, etc. Added to CONNECTION_CATEGORIES (geo), display type_labels/icons, export type_labels, recommendations type_to_category. Capped at 10 connections. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2248 → 2255. 48th intelligence feature.

### N-151: Geospatial & Mapping Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects geospatial and mapping libraries across Python (GeoPandas, Shapely, Fiona, rasterio, pyproj, GDAL, geopy, GeoAlchemy2, H3, Cartopy, OSMnx, xarray, Kepler.gl, GeoJSON, S2), JS/TS (Leaflet, Mapbox GL, MapLibre GL, OpenLayers, Cesium, Turf.js, Google Maps, React Leaflet, react-map-gl, H3, GeoJSON, HERE Maps), Go (orb, S2 Geometry, go-geom, Tile38, H3), Rust (geo, geozero, proj, H3, S2), Java (GeoTools, JTS, Spatial4j, H3, GraphHopper). TechStack field, portfolio summary, project card, CSV/MD/JSON export, CLI search. 17 tests.
**Shipped**: 2026-03-21. Total test count: 2231 → 2248. 48th detection category.

### N-150: Doctor Sort Command
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--sort` option to `atlas doctor` command. Supports sorting by priority (critical→high→medium→low) and category (alphabetical). Works with all existing filters (--category, --priority) and output formats (rich, json, csv). 3 tests.
**Shipped**: 2026-03-21. Total test count: 2228 → 2231. 47th experience feature.

### N-149: Data Visualization Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project data visualization intelligence. Detects shared viz libs (shared_data_viz — info) and interactive vs static paradigm divergence (data_viz_divergence — warning). Interactive: Dash, Streamlit, Gradio, Bokeh, D3.js, ECharts, Recharts, Chart.js, etc. Static: Matplotlib, Seaborn, Altair, Plotters, JFreeChart, etc. Added to CONNECTION_CATEGORIES (dataviz), display type_labels/icons, export type_labels, recommendations type_to_category. Capped at 10 connections. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2221 → 2228. 47th intelligence feature.

### N-148: Data Visualization Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects data visualization and charting libraries across Python (Matplotlib, Plotly, Seaborn, Bokeh, Altair, Folium, plotnine, Pygal, HoloViews, hvPlot, Panel, Dash, Streamlit, Gradio, pydeck, bqplot, Mayavi, VisPy, pyecharts, Plotext), JS/TS (D3.js, Chart.js, Recharts, Nivo, Victory, Visx, ECharts, Highcharts, ApexCharts, Plotly.js, Three.js, Deck.gl, Observable Plot, Tremor, Frappe Charts, uPlot, Vega, Vega-Lite, Lightweight Charts, Ant Charts), Go (go-echarts, Gonum Plot, go-chart, termui, asciigraph), Rust (Plotters, plotlib, charming, textplots), Java (JFreeChart, XChart, JavaFX Charts, Processing). TechStack field, portfolio summary, project card, CSV/MD/JSON export, CLI search. 19 tests.
**Shipped**: 2026-03-21. Total test count: 2202 → 2221. 47th detection category.

### N-147: Connections Sort Command
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--sort` option to `atlas connections` command. Supports sorting by type (alphabetical), severity (critical→warning→info), and projects (most involved first). Works with all existing filters (--type, --severity, --project) and output formats (rich, json, csv). 3 tests.
**Shipped**: 2026-03-21. Total test count: 2199 → 2202. 46th experience feature.

### N-146: PDF & Document Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects PDF and document generation libraries across Python (ReportLab, FPDF2, WeasyPrint, xhtml2pdf, pypdf, PyMuPDF, pdfplumber, PDFMiner, Camelot, tabula-py, pikepdf, borb, python-docx, openpyxl, XlsxWriter, python-pptx, Pandoc), JS/TS (PDFKit, pdf-lib, jsPDF, Puppeteer, Playwright, React-PDF, PDF.js, pdfmake, docx, ExcelJS, SheetJS, PapaParse, csv-parse), Go (UniPDF, gofpdf, goPDF, pdfcpu, Excelize), Rust (printpdf, genpdf, lopdf, pdf-extract, calamine), Java (iText, Apache PDFBox, OpenPDF, JasperReports, Apache POI). TechStack field, portfolio summary, project card, CSV/MD/JSON export, CLI search. 18 tests.
**Shipped**: 2026-03-21. Total test count: 2181 → 2199. 46th detection category.

### N-145: Cryptography Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects cryptography and encryption libraries across Python (cryptography, PyCryptodome, PyNaCl, bcrypt, Passlib, Argon2, pyOpenSSL, certifi, Paramiko, jwcrypto, truststore), JS/TS (CryptoJS, bcrypt.js, Argon2, jose, jsonwebtoken, node-forge, TweetNaCl, libsodium, OpenPGP.js, noble-curves, noble-hashes, scrypt-js), Go (x/crypto, age, CIRCL), Rust (ring, rustls, rcgen, Orion, sodiumoxide, Argon2, bcrypt, sha2, aes-gcm), Java (Bouncy Castle, Jasypt, Tink, Conscrypt, Spring Security Crypto). TechStack field, portfolio summary, project card, CSV/MD/JSON export, CLI search. 19 tests.
**Shipped**: 2026-03-21. Total test count: 2162 → 2181. 45th detection category.

### N-144: Image Processing Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project image processing intelligence. Detects shared image libs (shared_image_lib, info) and paradigm divergence — high-level (Pillow, Sharp, Jimp, imaging, Thumbnailator) vs low-level (OpenCV, GoCV, scikit-image, imageproc, pyvips, rawpy) (image_lib_divergence, warning). Added connection types, display icons/labels, CLI category "imaging", export labels, recommendation mapping. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2155 → 2162. 46th intelligence feature.

### N-143: Status Sort Command
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--sort` option to `atlas status` command. Supports sorting by name (alphabetical), health (descending), loc (descending), and grade (A→F, then alphabetical). Works with all existing filters (--grade, --lang, --has, --min-health, --max-health) and output formats (rich, json, csv). 3 tests.
**Shipped**: 2026-03-21. Total test count: 2152 → 2155. 45th experience feature.

### N-142: Date & Time Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project date/time intelligence. Detects shared date/time libs (shared_date_lib, info) and paradigm divergence — modern (Day.js, date-fns, Luxon, Temporal, Arrow, Pendulum, chrono) vs legacy (Moment.js, Joda-Time, python-dateutil, pytz) (date_lib_divergence, warning). Added connection types, display icons/labels, CLI category "datetime", export labels, recommendation mapping. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2145 → 2152. 45th intelligence feature.

### N-141: Image Processing Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects image processing libraries across Python (Pillow, OpenCV, scikit-image, imageio, Wand, CairoSVG, pyvips, rawpy), JS/TS (Sharp, Jimp, node-canvas, napi-canvas, GraphicsMagick, image-size, pngjs, pixelmatch, BlurHash, Plaiceholder, IMG.LY, Cropper.js), Go (imaging, gg, nfnt/resize, bild, GoCV, x/image), Rust (image, imageproc, resvg, OpenCV), Java (Thumbnailator, imgscalr, TwelveMonkeys, Scrimage). TechStack field, portfolio summary, project card, CSV/MD/JSON export, CLI search. 21 tests.
**Shipped**: 2026-03-21. Total test count: 2125 → 2145. 44th detection category.

### N-140: Top Projects CSV Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format csv` to `atlas top` command. Outputs CSV with Rank, Name, metric value, Grade, Stack columns. Works with --by (health, loc, tests, commits) and --limit options. 3 tests.
**Shipped**: 2026-03-21. Total test count: 2122 → 2125. 44th experience feature.

### N-139: Payment & Billing Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project payment intelligence. Detects shared payment tools (shared_payment_tool, info) and paradigm divergence — traditional (Stripe, PayPal, etc.) vs merchant-of-record (Paddle, Lemon Squeezy, etc.) (payment_divergence, warning). Added connection types, display icons/labels, CLI category "payments", export labels, recommendation mapping. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2115 → 2122. 44th intelligence feature.

### N-138: Date & Time Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects date/time libraries across Python (Arrow, Pendulum, python-dateutil, pytz, humanize, dateparser, iso8601, ciso8601), JS/TS (Day.js, date-fns, Luxon, Moment.js, Spacetime, Temporal, timeago.js, chrono-node, ms, Fecha, Tempo), Go (jinzhu/now, dateparse, iso8601, rickb777/date), Rust (chrono, time, humantime), Java (Joda-Time, ThreeTen-Extra, PrettyTime). TechStack field, portfolio summary, project card, CSV/MD/JSON export, CLI search. 22 tests.
**Shipped**: 2026-03-21. Total test count: 2093 → 2115. 43rd detection category.

### N-137: Compare CSV Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format csv` to `atlas compare` command. Outputs CSV with Metric/ProjectA/ProjectB/Delta columns. Rows cover Grade, Health%, Tests%, Git%, Docs%, Structure%, LOC, Source Files, Test Files, Commits, Languages, Frameworks, License. 3 tests.
**Shipped**: 2026-03-21. Total test count: 2090 → 2093. 43rd experience feature.

### N-136: Status CSV Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format csv` to `atlas status` command. Outputs CSV with Name, Path, Grade, Health%, Tests%, Git%, Docs%, Structure%, Languages, Frameworks, LOC, Source Files, Test Files, License columns. Works with all existing filters (--grade, --lang, --has, --min-health, --max-health). Empty filter returns header-only CSV. 3 tests.
**Shipped**: 2026-03-21. Total test count: 2087 → 2090. 42nd experience feature.

### N-135: Payment & Billing Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Detects payment and billing libraries across Python (Stripe, PayPal, Braintree, Square, Adyen, Paddle, Razorpay, Mollie, Coinbase Commerce, GoCardless, Paystack, Flutterwave, Lemon Squeezy), JS/TS (Stripe, PayPal, Braintree, Square, Adyen, Paddle, Razorpay, Mollie, Recurly, Chargebee, Lemon Squeezy), Go (Stripe, PayPal, Braintree, Adyen, Razorpay), Rust (async-stripe), Java (Stripe, PayPal, Braintree, Adyen, Square, Razorpay). Added TechStack field, portfolio summary, project card, CSV/markdown/JSON export, CLI search. 26 tests.
**Shipped**: 2026-03-21. Total test count: 2061 → 2087. 42nd detection category.

### N-134: Event Streaming Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project event streaming intelligence. Detects shared streaming tools (shared_event_streaming, info) and paradigm divergence — kafka-based vs amqp-based vs cloud-managed (event_streaming_divergence, warning). Added connection types, display icons/labels, CLI category "streaming", export labels, recommendation mapping. 8 tests.
**Shipped**: 2026-03-21. Total test count: 2053 → 2061. 43rd intelligence feature.

### N-133: Status Grade Distribution
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--grades` flag to `atlas status` command. Shows compact grade distribution with Unicode bar chart (A/B+/B/C/D/F counts). Supports `--format json` for structured output with total and grades object. Works with all existing filters (--grade, --lang, --has, --min-health, --max-health). 3 tests.
**Shipped**: 2026-03-21. Total test count: 2050 → 2053. 41st experience feature.

### N-132: Event Streaming Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_event_streaming()` in detector.py. Detects event streaming/message broker libraries across ecosystems: Python (Confluent Kafka, kafka-python, aiokafka, RabbitMQ pika/aio-pika, Kombu, NATS, Apache Pulsar, Faust), JS/TS (KafkaJS, RabbitMQ amqplib, AMQP rhea, NATS, BullMQ, Google Pub/Sub, AWS SQS/SNS/Kinesis, Azure Event Hubs/Service Bus), Go (kafka-go, Sarama, RabbitMQ, NATS, Apache Pulsar, Watermill), Rust (rdkafka, lapin, async-nats, pulsar), Java (Spring Kafka/AMQP/RabbitMQ, Kafka Clients, NATS, Azure). Added `event_streaming` field to TechStack model. Shows in project card, portfolio summary, all exports. 24 detection tests.
**Shipped**: 2026-03-21. Total test count: 2026 → 2050. 41st detection category.

### N-131: GraphQL Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project GraphQL intelligence: shared GraphQL libs (shared_graphql_lib), server-first vs client-first paradigm divergence (graphql_divergence). No gap type (GraphQL is architectural preference). New CONNECTION_CATEGORIES entry "graphql" (41 total). Updated display type_labels, icons, stats category mapping, export type_labels, recommendations mapping. 7 tests.
**Shipped**: 2026-03-21. Total test count: 2019 → 2026. 42nd intelligence feature.

### N-130: Doctor Priority Filter
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--priority` / `-p` option to `atlas doctor` command. Filters recommendations by priority level (critical, high, medium, low). Validates input with error message for unknown priorities. Works with all output formats (rich, json, csv) and combines with existing --category filter. 3 tests.
**Shipped**: 2026-03-21. Total test count: 2016 → 2019. 40th experience feature.

### N-129: GraphQL Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_graphql_libs()` in detector.py. Detects GraphQL libraries across ecosystems: Python (Graphene, Graphene-Django, Ariadne, Strawberry, sgqlc, gql, graphql-core, Tartiflette), JS/TS (graphql-js, Apollo Server, Apollo Client, GraphQL Yoga, TypeGraphQL, Nexus, GraphQL Code Generator, graphql-request, URQL, Relay, Mercurius, Pothos, graphql-tools, graphql-tag), Go (gqlgen, graphql-go, graph-gophers, Thunder, genqlient), Rust (Juniper, async-graphql, graphql-client, Cynic), Java (graphql-java, GraphQL Spring, Netflix DGS, SmallRye GraphQL, graphql-kotlin). Also detects .graphql/.gql schema files. Added `graphql_libs` field to TechStack model. Shows in project card, portfolio summary, all exports. 25 detection tests.
**Shipped**: 2026-03-21. Total test count: 1996 → 2016. 40th detection category.

### N-128: Connections Summary Mode
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--summary` flag to `atlas connections` command. Shows compact Rich table with category names, total counts, and severity breakdown (critical/warning/info columns). Supports `--format json` for structured output with categories object. Works with all existing filters (--type, --severity, --project). 3 tests.
**Shipped**: 2026-03-21. Total test count: 1993 → 1996. 39th experience feature.

### N-127: WebSocket Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project WebSocket intelligence: shared WebSocket libs (shared_websocket_lib), managed vs self-hosted paradigm divergence (websocket_divergence). No gap type (WebSocket is architectural preference). New CONNECTION_CATEGORIES entry "websocket". Updated display type_labels, icons, stats category mapping, export type_labels, recommendations mapping. 7 tests.
**Shipped**: 2026-03-21. Total test count: 1986 → 1993. 41st intelligence feature.

### N-126: WebSocket Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_websocket_libs()` in detector.py. Detects WebSocket/real-time libraries across ecosystems: Python (websockets, python-socketio, Django Channels, Starlette WebSocket, Tornado WebSocket, Autobahn, aiohttp WebSocket, wsproto), JS/TS (Socket.IO, ws, SockJS, Primus, tRPC WebSocket, graphql-ws, Pusher, Ably, Action Cable, Centrifugo), Go (Gorilla WebSocket, nhooyr/websocket, gobwas/ws, Melody), Rust (Tungstenite, Axum/Actix/Warp WebSocket), Java (Spring WebSocket, Jakarta WebSocket, Tyrus, Netty WebSocket). Added `websocket_libs` field to TechStack model. Shows in project card, portfolio summary, all exports. 17 detection tests.
**Shipped**: 2026-03-21. Total test count: 1969 → 1986. 39th detection category.

### N-125: Connections Project Filter
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--project` option to `atlas connections` command. Filters connections to only those involving a specific project (case-insensitive match). Works with all output formats (rich, JSON, CSV) and combines with existing --type and --severity filters. Enables per-project connection analysis. 3 tests.
**Shipped**: 2026-03-21. Total test count: 1966 → 1969. 38th experience feature.

### N-124: Dependency Injection Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project DI framework intelligence: shared DI frameworks (shared_di_framework), container-based vs implicit paradigm divergence (di_divergence). No gap type (DI is architectural preference). New CONNECTION_CATEGORIES entry "di". Updated display type_labels, icons, stats category mapping, export type_labels, recommendations mapping. 7 tests.
**Shipped**: 2026-03-21. Total test count: 1959 → 1966. 40th intelligence feature.

### N-123: Dependency Injection Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_di_frameworks()` in detector.py. Detects DI/IoC frameworks across ecosystems: Python (dependency-injector, python-inject, Lagom, punq, wireup, svcs, dishka, FastAPI Depends), JS/TS (InversifyJS, tsyringe, TypeDI, Awilix, BottleJS, injection-js, Angular DI, NestJS DI), Go (Uber Fx, Uber Dig, Wire, do), Rust (Shaku, inject), Java (Spring DI, Google Guice, Dagger, CDI, Micronaut DI, Quarkus CDI). Added `di_frameworks` field to TechStack model. Shows in project card, portfolio summary, all exports. 18 detection tests.
**Shipped**: 2026-03-21. Total test count: 1941 → 1959. 38th detection category.

### N-122: Doctor Category Filter
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--category` option to `atlas doctor` command. Filters recommendations by category (tests, docs, git, infra, quality, security, structure, deps). Works with all output formats: rich terminal, JSON, and CSV. Enables focused health analysis on specific areas. 3 tests.
**Shipped**: 2026-03-21. Total test count: 1938 → 1941. 37th experience feature.

### N-121: Serialization Format Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project serialization format intelligence: shared serialization formats (shared_serialization_format), binary vs text-based paradigm divergence (serialization_divergence). No gap type (serialization is optional). New CONNECTION_CATEGORIES entry "serialization". Updated display type_labels, icons, stats category mapping, export type_labels, recommendations mapping. 7 tests.
**Shipped**: 2026-03-21. Total test count: 1931 → 1938. 39th intelligence feature.

### N-120: Serialization Format Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_serialization_formats()` in detector.py. Detects serialization/interchange formats across ecosystems: Python (Protocol Buffers, MessagePack, Apache Avro, Thrift, FlatBuffers, CBOR, YAML, TOML, orjson, ujson, Pydantic, Marshmallow, cattrs, Pickle, Apache Arrow, Parquet, BSON), JS/TS (protobufjs, js-yaml, BSON, Apache Arrow, superjson), Go (protobuf, msgpack, yaml, toml, go-json, Apache Avro, Arrow), Rust (serde_json, simd-json, Bincode, Postcard, prost, rmp, cbor, yaml, toml), Java (Jackson, Gson, protobuf, Avro, Kryo, Thrift, Parquet, Arrow). Also detects .proto and .avsc files. Added `serialization_formats` field to TechStack model. Shows in project card, portfolio summary, all exports. 26 detection tests.
**Shipped**: 2026-03-21. Total test count: 1905 → 1931. 37th detection category.

### N-119: Search JSON Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format json` option to `atlas search` command. Outputs structured JSON with `query`, `total` count, and `projects` array (name, path, health_grade, health_percent, languages, frameworks, loc, license). Enables programmatic search integration. 2 tests.
**Shipped**: 2026-03-21. Total test count: 1903 → 1905. 36th experience feature.

### N-118: Template Engine Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project template engine intelligence: shared template engines (shared_template_engine), string-based vs component-based paradigm divergence (template_engine_divergence). No gap type (template engines are optional). New CONNECTION_CATEGORIES entry "templates". Updated display type_labels, icons, stats category mapping, export type_labels, recommendations mapping. 7 tests.
**Shipped**: 2026-03-21. Total test count: 1896 → 1903. 38th intelligence feature.

### N-117: Template Engine Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_template_engines()` in detector.py. Detects template engines across ecosystems: Python (Jinja2, Mako, Chameleon, Genshi, Cheetah, Django Templates), JS/TS (Handlebars, EJS, Pug, Nunjucks, Mustache, Liquid, Eta, Marko, Edge.js, Vue SFC, Svelte, Solid, Astro), Go (Pongo2, Raymond, Jet, Amber), Rust (Tera, Askama, Handlebars, MiniJinja, Maud), Java (Thymeleaf, FreeMarker, Velocity, Mustache, Pebble). Added `template_engines` field to TechStack model. Shows in project card, portfolio summary, all exports. 20 detection tests.
**Shipped**: 2026-03-21. Total test count: 1876 → 1896. 36th detection category.

### N-116: Top Projects JSON Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format json` option to `atlas top` command. Outputs structured JSON with `metric` (sort field), `limit`, and `projects` array (rank, name, value, health_grade, stack summary). Works with --by and --limit options. 2 tests.
**Shipped**: 2026-03-21. Total test count: 1874 → 1876. 35th experience feature.

### N-115: Caching Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project caching intelligence: shared caching tools (shared_caching_tool), Redis-based vs in-memory paradigm divergence (caching_divergence), caching gaps for backend projects with databases and 10+ source files (caching_gap). New CONNECTION_CATEGORIES entry "caching". Updated display type_labels, icons, stats category mapping, export type_labels, recommendations mapping. 10 tests.
**Shipped**: 2026-03-21. Total test count: 1864 → 1874. 37th intelligence feature.

### N-114: Caching Library Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_caching_tools()` in detector.py. Detects caching libraries across ecosystems: Python (redis-py, cachetools, DiskCache, django-redis, Flask-Caching, aiocache, cashews, dogpile.cache, pymemcache, pylibmc, CacheControl), JS/TS (ioredis, redis Node, node-cache, lru-cache, Keyv, cache-manager, Memcached Node, catbox), Go (go-redis, Ristretto, BigCache, groupcache, FreeCache, GCache, gomemcache), Rust (moka, cached, redis-rs, mini-moka), Java (Caffeine, Ehcache, Spring Cache, Jedis, Lettuce, Redisson, Guava Cache, Hazelcast). Added `caching_tools` field to TechStack model. Shows in project card, portfolio summary, all exports. 21 detection tests.
**Shipped**: 2026-03-21. Total test count: 1843 → 1864. 35th detection category.

### N-113: Compare JSON Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format json` option to `atlas compare` command. Outputs structured JSON with `project_a`/`project_b` summaries (name, path, health object, loc, source/test files, commits, languages, frameworks, license), `deltas` (health_percent, loc, source_files, test_files, commits), `shared_frameworks`, `unique_frameworks_a`, `unique_frameworks_b`, `shared_deps`. 3 tests.
**Shipped**: 2026-03-21. Total test count: 1840 → 1843. 34th experience feature.

### N-112: Configuration Management Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project configuration management intelligence: shared config tools (shared_config_tool), env-based vs structured paradigm divergence (config_tool_divergence — env_based: dotenv/decouple/envalid/etc vs structured: Hydra/Viper/Convict/etc), config tool gaps for backend projects with 5+ source files (config_tool_gap). New CONNECTION_CATEGORIES entry "config". Updated display type_labels, icons, stats category mapping, export type_labels, recommendations mapping. 10 tests.
**Shipped**: 2026-03-21. Total test count: 1830 → 1840. 36th intelligence feature.

### N-111: Configuration Management Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_config_tools()` in detector.py. Detects configuration management tools across ecosystems: Python (python-dotenv, Dynaconf, Hydra, OmegaConf, Pydantic Settings, python-decouple, environs, Everett, Confuse, ConfigObj), JS/TS (dotenv, Convict, node-config, envalid, env-cmd, cross-env, nconf, cosmiconfig, rc, t3-env), Go (Viper, envconfig, godotenv, koanf, env, cleanenv), Rust (config-rs, dotenvy, Figment, envy), Java (Spring Config, Typesafe Config, Commons Configuration, dotenv-java). Also detects .env/.env.example files. Added `config_tools` field to TechStack model. Shows in project card, portfolio summary, all exports. 23 detection tests.
**Shipped**: 2026-03-21. Total test count: 1807 → 1830. 34th detection category.

### N-110: Status JSON Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format json` option to `atlas status` command. Outputs structured JSON with `total` count and `projects` array (name, path, health object with grade/percent/tests/git_hygiene/documentation/structure, languages, frameworks, LOC, source/test files, license). Works with all existing filters (--grade, --lang, --has, --min-health, --max-health). Returns empty array for no-match filters. 3 tests.
**Shipped**: 2026-03-21. Total test count: 1804 → 1807. 33rd experience feature.

### N-109: CLI Framework Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project CLI framework intelligence: shared CLI frameworks (shared_cli_framework), declarative vs TUI paradigm divergence (cli_framework_divergence). New CONNECTION_CATEGORIES entry "cli". 7 tests.
**Shipped**: 2026-03-21. Total test count: 1797 → 1804. 35th intelligence feature.

### N-108: CLI Framework Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_cli_frameworks()` in detector.py. Detects CLI framework libraries across ecosystems: Python (Click, Typer, Fire, Rich, Textual, Cement, cliff, docopt, plac, Cleo, prompt_toolkit, Questionary, InquirerPy, Trogon), JS/TS (Commander.js, Yargs, meow, oclif, Vorpal, Caporal, Inquirer.js, prompts, Chalk, Ora, Ink, citty, Clipanion, Gluegun), Go (Cobra, urfave/cli, pflag, Kong, Bubbletea, Lip Gloss, Huh, go-flags), Rust (clap, StructOpt, argh, dialoguer, indicatif, console, Ratatui), Java (picocli, JCommander, Airline, Spring Shell). Added `cli_frameworks` field to TechStack model. Shows in project card, portfolio summary, all exports. 20 detection tests.
**Shipped**: 2026-03-21. Total test count: 1777 → 1797. 33rd detection category.

### N-107: Doctor CSV Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format csv` option to `atlas doctor` command. Outputs CSV with Priority, Category, Message, Projects columns. 2 tests.
**Shipped**: 2026-03-21. Total test count: 1775 → 1777. 32nd experience feature.

### N-106: Documentation Generation Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project documentation generation intelligence: shared doc generators (shared_doc_generator), static-site vs API-docs vs component-docs vs config-docs paradigm divergence (doc_generator_divergence), doc generator gaps for projects with 20+ source files (doc_generator_gap). New CONNECTION_CATEGORIES entry "docgen". 10 tests.
**Shipped**: 2026-03-21. Total test count: 1765 → 1775. 34th intelligence feature.

### N-105: Documentation Generation Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_doc_generators()` in detector.py. Detects documentation generation tools: Python (Sphinx, MkDocs, pdoc, pydoctor), JS/TS (Docusaurus, Storybook, VitePress, TypeDoc, JSDoc, Nextra, GitBook, Docsify, Mintlify, Starlight, documentation.js), Rust (mdBook, rustdoc), Go (Swag), Java (Javadoc, Dokka), generic (Doxygen). Detects via dependency files, config files (docusaurus.config.js, .storybook/, book.toml, Doxyfile, typedoc.json, mkdocs.yml, docs/conf.py), and directory markers. Added `doc_generators` field to TechStack model. Shows in project card, portfolio summary, all exports. 20 detection tests.
**Shipped**: 2026-03-21. Total test count: 1745 → 1765. 32nd detection category.

### N-104: Connections CSV Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format csv` option to `atlas connections` command. Outputs CSV with Type, Detail, Projects, Severity columns. Filter messages suppressed in CSV mode. Works with `--type` and `--severity` filters. 2 tests.
**Shipped**: 2026-03-21. Total test count: 1743 → 1745. 31st experience feature.

### N-103: HTTP Client Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project HTTP client intelligence: shared HTTP clients (shared_http_client), sync vs async vs fetch-based vs RPC-style paradigm divergence (http_client_divergence), HTTP client gaps for backend projects (http_client_gap). New CONNECTION_CATEGORIES entry "http". 10 tests.
**Shipped**: 2026-03-21. Total test count: 1733 → 1743. 33rd intelligence feature.

### N-102: HTTP Client Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_http_clients()` in detector.py. Detects HTTP client libraries across ecosystems: Python (Requests, HTTPX, aiohttp, urllib3, httplib2, PycURL, treq, asks, niquests, Uplink), JS/TS (Axios, node-fetch, Got, Ky, SuperAgent, Undici, ofetch, Wretch, Needle, cross-fetch, isomorphic-fetch), Go (Resty, go-retryablehttp, Gentleman, Sling, Heimdall, Req), Rust (reqwest, hyper, ureq, surf, isahc, attohttpc), Java (OkHttp, Apache HttpClient, Retrofit, Unirest, WebClient, RestTemplate, Feign). Added `http_clients` field to TechStack model. Shows in project card, portfolio summary, all exports. 21 detection tests.
**Shipped**: 2026-03-21. Total test count: 1712 → 1733. 31st detection category.

### N-101: Connections JSON Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added `--format json` option to `atlas connections` command. Outputs structured JSON with `total` count, `connections` array (type, detail, projects, severity per connection), and `summary` (severity counts: critical/warning/info). Filter messages suppressed in JSON mode. Works with `--type` and `--severity` filters. 3 tests.
**Shipped**: 2026-03-21. Total test count: 1709 → 1712. 30th experience feature.

### N-100: Feature Flag Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project feature flag intelligence: shared feature flag tools (shared_feature_flag), SaaS vs self-hosted vs analytics vs standard paradigm divergence (feature_flag_divergence), feature flag gaps for web projects (feature_flag_gap). New CONNECTION_CATEGORIES entry "flags". 10 tests.
**Shipped**: 2026-03-21. Total test count: 1699 → 1709. 32nd intelligence feature.

### N-99: Feature Flag Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_feature_flags()` in detector.py. Detects feature flag and experimentation tools across ecosystems: Python (LaunchDarkly, Unleash, Flagsmith, GrowthBook, Split, PostHog, Statsig, OpenFeature, Waffle, Flask-FeatureFlags), JS/TS (LaunchDarkly, Unleash, Flagsmith, GrowthBook, Split, PostHog, Statsig, OpenFeature, HappyKit, Vercel Flags, ConfigCat), Go (LaunchDarkly, Unleash, GrowthBook, OpenFeature, PostHog), Rust (LaunchDarkly, Unleash, OpenFeature), Java (LaunchDarkly, Unleash, Flagsmith, GrowthBook, Split, OpenFeature, Togglz, FF4J). Added `feature_flags` field to TechStack model. Shows in project card, portfolio summary, all exports. 21 detection tests.
**Shipped**: 2026-03-21. Total test count: 1678 → 1699. 30th detection category.

### N-51: Build Tool Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project build tool pattern detection via `_find_build_tool_patterns()` in connections.py. Analyzes build_tools data from N-50 across the portfolio to detect: shared build tools (Make/tox across 2+ projects, info), Python task runner divergence (tox vs nox vs Invoke vs doit across portfolio, warning), Java build tool divergence (Gradle vs Maven across portfolio, warning), and build automation gaps (projects with 10+ source files but no build/task automation, warning). New connection types (`shared_build_tool`, `build_tool_divergence`, `build_tool_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps build_tool_gap to `infra` and build_tool_divergence to `infra` recommendation categories. 13 build tool pattern tests.
**Shipped**: 2026-03-21. Total test count: 966 → 979. Completes N-50 detection→intelligence pipeline. All 13 detection→intelligence pipelines complete.

### N-50: Build & Task Runner Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_build_tools()` in detector.py. Detects build tools and task runners across ecosystems: generic (Make, Taskfile/go-task, Just, Earthly), Python (tox, nox, Invoke, doit), JavaScript (npm scripts via package.json scripts section), Java/JVM (Gradle, Maven), C/C++ (CMake, Meson), polyglot (Bazel), Ruby (Rake). Returns sorted list. Added `build_tools` field to TechStack model. Shows in `atlas inspect` project card, portfolio summary panel (display.py), markdown export project details and summary, JSON export portfolio_summary, and CSV export. `_project_has_tech()` searches build_tools. 24 detection tests.
**Shipped**: 2026-03-21. Total test count: 942 → 966. 13th detection category.

### N-49: CSV Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: New `build_csv_report()` in export_report.py. Generates CSV portfolio reports — one row per project with 28 columns: Name, Path, Health % and Grade, 4 health dimension scores (Tests/Git/Docs/Structure as 0-100), file counts (source/test/total/LOC), all 12 tech stack fields (semicolon-delimited lists), runtime versions (key=value pairs), license, and git info (branch/last commit/commits). Added `--format csv` option to `atlas export` command. CSV stdout uses `print()` to avoid Rich markup. Ideal for importing into spreadsheets or data analysis tools. 8 CSV export unit tests + 2 CLI integration tests.
**Shipped**: 2026-03-21. Total test count: 932 → 942. Third export format alongside markdown and JSON.

### N-48: Runtime Version Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project runtime version pattern detection via `_find_runtime_version_patterns()` in connections.py. Analyzes runtime_versions data from N-47 across the portfolio to detect: shared runtime versions (Python/Node pinned in 2+ projects, info), runtime version divergence (same language with different versions across projects — e.g., Python 3.12 vs 3.11, warning), and runtime version pinning gaps (projects with 5+ source files but no pinned runtime version when other projects have them, warning). New connection types (`shared_runtime`, `runtime_divergence`, `runtime_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps runtime_gap to `infra` and runtime_divergence to `deps` recommendation categories. 12 runtime version pattern tests.
**Shipped**: 2026-03-21. Total test count: 920 → 932. Completes N-47 detection→intelligence pipeline. All 12 detection→intelligence pipelines complete.

### N-45: CI/CD Configuration Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project CI/CD configuration pattern detection via `_find_ci_config_patterns()` in connections.py. Analyzes ci_config data from N-43 across the portfolio to detect: shared CI/CD configuration items (GitHub Actions/pre-commit across 2+ projects, info), dependency update strategy divergence (Dependabot config vs Renovate config across portfolio, warning), and CI/CD configuration gaps — PR template gap (projects with CI but no PR template, >10 source files, warning), CODEOWNERS gap (projects with >20 source files but no CODEOWNERS, warning), pre-commit gap (projects with quality tools but no pre-commit hooks, warning). New connection types (`shared_ci_config`, `ci_config_divergence`, `ci_config_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps to `infra` recommendation category. 17 CI/CD configuration pattern tests.
**Shipped**: 2026-03-21. Total test count: 877 → 894. Completes N-43 detection→intelligence pipeline. 13th intelligence layer.

### N-43: CI/CD Configuration Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_ci_config()` in detector.py. Detects CI/CD configuration and workflow artifacts: GitHub Actions workflows (with release/deploy pattern detection), GitLab CI, PR templates (file + directory forms), issue templates, CODEOWNERS (3 locations), Dependabot config, Renovate config (4 file variants), pre-commit hooks, git hooks (.husky/.githooks directories), and .gitattributes. Added `ci_config` field to TechStack model. Shows in `atlas inspect` project card, portfolio summary panel (display.py and export_report.py), markdown export project details, and JSON export portfolio_summary. 18 new detection tests, 3 display tests.
**Shipped**: 2026-03-21. Total test count: 850 → 871. 11th detection category.

### N-42: Documentation Artifacts Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project documentation artifact pattern detection via `_find_docs_artifact_patterns()` in connections.py. Analyzes docs_artifacts data from N-41 across the portfolio to detect: shared documentation artifacts (README/CHANGELOG/LICENSE across 2+ projects, info), documentation coverage divergence (projects with 5+ artifacts vs projects with ≤1 artifact and 5+ source files, warning), and documentation gaps — README missing (critical, >5 source files), CHANGELOG missing (warning, >10 source files), CONTRIBUTING missing (warning, >20 source files). New connection types (`shared_docs`, `docs_divergence`, `docs_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps to `docs` recommendation category. 17 documentation pattern tests.
**Shipped**: 2026-03-21. Total test count: 833 → 850. Completes N-41 detection→intelligence pipeline. 9th intelligence layer.

### N-41: Documentation Artifacts Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_docs_artifacts()` in detector.py. Detects documentation artifacts present in projects: README (md/rst/txt), CHANGELOG (also CHANGES/HISTORY variants), CONTRIBUTING, CODE_OF_CONDUCT, SECURITY policy, LICENSE file, docs/ directory, API specs (OpenAPI/Swagger JSON/YAML — checks root and docs/ subdirectory), and .editorconfig. Returns sorted list of artifact names. Added `docs_artifacts` field to TechStack model. Shows in `atlas inspect` project card, markdown export project details, portfolio summary panel (display.py and export_report.py), and JSON export portfolio_summary. 17 new detection tests, 3 display tests. Distinct from health.py documentation scoring — health gives a numeric score for README/CHANGELOG/docs/CLAUDE.md presence; docs_artifacts provides a detailed inventory of specific documentation artifacts.
**Shipped**: 2026-03-21. Total test count: 813 → 833. 10th detection category.

### N-40: Enhanced JSON Export
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Comprehensive JSON export via `build_json_report()` in export_report.py. Replaces the basic inline JSON generation in cli.py. Now includes: portfolio summary aggregates (languages, frameworks, infra, security, quality, testing, databases, package managers, AI/ML, licenses — all as structured data), cross-project connections (type, detail, projects, severity), and doctor recommendations (priority, category, message, projects). Per-project data includes license field. Uses raw `print()` for JSON stdout to avoid Rich markup corruption. 14 new JSON export tests.
**Shipped**: 2026-03-21. Total test count: 799 → 813. JSON export now at full parity with markdown export.

### N-39: License Summary Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added license distribution stats to the portfolio summary panel (display.py) and markdown export (export_report.py). Shows `Licenses: X/N projects · MIT (3), Apache-2.0 (2)` with top licenses ranked by usage. Row hidden when no projects have detected licenses. 6 new tests (3 display, 3 export).
**Shipped**: 2026-03-21. Total test count: 793 → 799. Completes the detection→intelligence→summary pipeline for licenses (N-37→N-38→N-39). All 8 pipelines now have full summary panel visibility.

### N-38: License Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project license pattern detection via `_find_license_patterns()` in connections.py. Analyzes license data from N-37 across the portfolio to detect: shared licenses (MIT/Apache-2.0 across 2+ projects), license divergence with copyleft/permissive detection (GPL+MIT mix = critical severity, MIT+Apache = warning severity), and license gaps (projects with 5+ source files but no detected license). New connection types (`shared_license`, `license_divergence`, `license_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. Maps to `docs` recommendation category. 13 license pattern tests.
**Shipped**: 2026-03-21. Total test count: 780 → 793. Completes N-37 detection→intelligence pipeline. 8th intelligence layer.

### N-37: License Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_license()` in detector.py. Detects project licenses from three sources: config files (pyproject.toml `[project] license`, package.json `license`, Cargo.toml `[package] license`), and LICENSE/LICENCE/COPYING file content analysis. Recognizes 13 license families: MIT, Apache-2.0, GPL-2.0/3.0, AGPL-3.0, LGPL-2.1/3.0, BSD-2-Clause/3-Clause, ISC, MPL-2.0, Unlicense, CC0-1.0. SPDX normalization handles variant identifiers (e.g., `GPL-3.0-only` → `GPL-3.0`). Config files take priority over LICENSE file content. Added `license` field to Project model (not TechStack — license is project-level). Shows in `atlas inspect` and markdown export. 25 license detection tests.
**Shipped**: 2026-03-21. Total test count: 755 → 780. 9th detection category. Enables future license intelligence layer for compliance.

### N-36: Package Manager Summary Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added package manager adoption stats to the portfolio summary panel (display.py) and markdown export (export_report.py). Shows `Pkg Mgrs: X/N projects · Poetry (3), npm (2)` with top managers ranked by usage. Row hidden when no projects have package managers. 6 new tests (3 display, 3 export).
**Shipped**: 2026-03-21. Completes the detection→intelligence→summary pipeline for package managers (N-34→N-35→N-36). All 7 pipelines now have full summary panel visibility.

### N-34: Package Manager Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_package_managers()` in detector.py. Detects package managers and build tools across ecosystems: Python (pip, Poetry, PDM, uv, Pipenv, setuptools, Hatch, Flit), JavaScript/TypeScript (npm, Yarn, pnpm, Bun), Rust (Cargo), Go (Go Modules), Ruby (Bundler), Java/Kotlin (Maven, Gradle), .NET (NuGet), PHP (Composer). Detects via lockfiles, config files, and pyproject.toml build-system declarations. Smart deduplication — pip not added when Poetry/PDM/uv/Pipenv present. Added `package_managers` field to TechStack model. Shows in `atlas inspect` and markdown export. 25 package manager tests.
**Shipped**: 2026-03-21. Total test count: 711 → 736. 8th detection category.

### N-33: Database Summary Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added database adoption stats to the portfolio summary panel (display.py) and markdown export (export_report.py). Shows `Databases: X/N projects · PostgreSQL (3), Redis (2)` with top databases ranked by usage. Row hidden when no projects have databases. 6 new tests (3 display, 3 export).
**Shipped**: 2026-03-21. Total test count: 705 → 711. All detection categories now have portfolio summary panel visibility: languages, frameworks, infra, security, quality, testing, databases, AI/ML.

### N-32: Database Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Replaced `_find_shared_databases()` with `_find_database_patterns()` in connections.py. Keeps shared database detection (info) and adds: relational DB divergence (PostgreSQL vs MySQL across portfolio, SQLite excluded as dev DB), vector DB divergence (ChromaDB vs Pinecone), message broker divergence (RabbitMQ vs Kafka), and database gaps (web/API projects with FastAPI/Django/Express/etc but no database detected). New connection types (`database_divergence`, `database_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. 16 new database pattern tests (replacing 5 old shared-only tests = net +11).
**Shipped**: 2026-03-13. Total test count: 694 → 705. Completes N-31 detection→intelligence pipeline. All 6 detection→intelligence pipelines complete.

### N-31: Enhanced Database Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: Expanded `detect_databases()` from 5 to 21 databases/data stores. New categories: relational (MySQL/MariaDB, CockroachDB, PlanetScale, Supabase), document (Firestore, DynamoDB), search (Elasticsearch/OpenSearch), graph (Neo4j), time-series (InfluxDB), wide-column (Cassandra), cache (Memcached), vector (ChromaDB, Pinecone, Qdrant, Weaviate), message brokers (RabbitMQ/AMQP, Kafka). Expanded search to go.mod, Cargo.toml, Gemfile, pom.xml, build.gradle, requirements-dev.txt, .env.sample. Refactored to use `_add()` helper for deduplication. 21 new database detection tests.
**Shipped**: 2026-03-13. Total test count: 673 → 694. 4.2x expansion of database detection coverage.

### N-30: Testing Summary Panel
**Pillar**: EXPERIENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Added testing framework adoption stats to the portfolio summary panel (display.py) and markdown export (export_report.py). Shows `Testing: X/N projects · pytest (3), Jest (2)` with top frameworks ranked by usage. Row hidden when no projects have testing frameworks. Follows the established pattern from security/quality/AI/ML summary rows. 7 new tests (4 display, 3 export).
**Shipped**: 2026-03-13. Total test count: 666 → 673. Completes the summary panel — all detection categories now have portfolio-level visibility.

### N-29: Testing Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project testing framework pattern detection via `_find_testing_patterns()` in connections.py. Analyzes testing framework data from N-28 across the portfolio to detect: shared testing frameworks (pytest/Jest across 2+ projects), JS test runner divergence (Jest vs Vitest vs Mocha vs AVA), Python test runner divergence (pytest vs nose2 vs unittest2), and testing gaps (projects with 5+ source files but no testing framework). New connection types (`shared_testing`, `testing_divergence`, `testing_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. 15 testing pattern tests.
**Shipped**: 2026-03-13. Total test count: 651 → 666. Completes N-28 detection→intelligence pipeline. All 5 detection→intelligence pipelines complete: infra (N-17→N-18), security (N-19→N-23), quality (N-24→N-25), AI/ML (N-21→N-27), testing (N-28→N-29).

### N-28: Testing Framework Detection
**Pillar**: DETECTION | **Status**: SHIPPED | **Priority**: P1
**What**: New `detect_testing_frameworks()` in detector.py. Detects testing frameworks and tools across projects: Python (pytest, tox, nox, Hypothesis, coverage.py, nose2), JavaScript/TypeScript (Jest, Vitest, Mocha, Cypress, Playwright, AVA, Testing Library), Go (go test from _test.go files), Rust (cargo test from Cargo.toml). Reads config files (pytest.ini, jest.config.*, vitest.config.*, .mocharc.*, cypress.config.*, playwright.config.*), dependency files, and conftest.py. Added `testing_frameworks` field to TechStack model. Shows in `atlas inspect` and markdown export. 30 testing framework tests.
**Shipped**: 2026-03-13. Total test count: 621 → 651. Separates testing tools from general frameworks for dedicated visibility.

### N-27: AI/ML Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project AI/ML pattern detection via `_find_ai_patterns()` in connections.py. Analyzes AI/ML tooling from N-21 across the portfolio to detect: shared AI/ML tools (Anthropic SDK/LangChain across 2+ projects), LLM provider divergence (Anthropic vs OpenAI across portfolio), vector DB divergence (ChromaDB vs Pinecone), and experiment tracking gaps (ML projects using PyTorch/TensorFlow/sklearn without MLflow/W&B/DVC). New connection types (`shared_ai`, `ai_divergence`, `ai_gap`) displayed in `atlas connections`, markdown export, and `atlas doctor`. 15 AI pattern tests.
**Shipped**: 2026-03-13. Total test count: 606 → 621. Completes N-21 detection→intelligence pipeline. Completes all 4 detection→intelligence pipelines: infra (N-17→N-18), security (N-19→N-23), quality (N-24→N-25), AI/ML (N-21→N-27).

### N-18: Infrastructure Intelligence
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Cross-project infrastructure pattern detection via `_find_infra_patterns()` in connections.py. Analyzes infrastructure data from N-17 across the portfolio to detect: shared infrastructure (Docker/CI across 2+ projects), platform divergence (multiple hosting platforms per project), CI divergence (multiple CI systems across portfolio), no-CI gaps, cloud usage without IaC, Docker without orchestration. New connection types (`shared_infra`, `infra_divergence`, `infra_gap`) displayed in `atlas connections`. 16 infra pattern tests.
**Shipped**: 2026-03-13. Total test count: 395 → 410. Builds on N-17 detection data.

### N-11: CLI Integration Tests
**Pillar**: INTELLIGENCE | **Status**: SHIPPED | **Priority**: P1
**What**: Full integration test coverage for every CLI command — init, add, scan, status, connections, inspect, remove, batch-add, export, license, activate, support, reset. 36 tests covering happy paths, error cases, edge cases (duplicate adds, missing portfolios, case-insensitive lookups, dot-dir exclusion, file export, reset confirmation/cancel).
**Shipped**: 2026-03-13. Total test count: 248 → 284. Every user-facing command now has test coverage.

---

## Status Lifecycle

```
IDEA --> RESEARCHED --> DECIDED --> BUILDING --> SHIPPED
  |          |              |           |
  +----------+--------------+-----------+--> ARCHIVED
```

---

## ASIF Governance

This project is governed by the ASIF portfolio. On every session:
1. Read `.asif/NEXUS.md` — check for `## CoS Directives` section

### DIRECTIVE-NXTG-20260418-03 — P2: Voice Identity Adoption
**From**: NXTG-AI CoS (Wolf) — Asif-initiated | **Priority**: P2
**Injected**: 2026-04-18 13:48 PDT | **Estimate**: S (under 30 min) | **Status**: PENDING

**Context**: PP (P-04) just shipped the portfolio voice service (`http://100.123.83.34:8880`). Asif directive: every team picks its own voice, owns it, and uses it always — no duplicates, no silent completion, no generic TTS fallback. Voice is team identity.

**Your voice**: `am_adam`
**Rationale**: Architect-vibe — portfolio intelligence / repo atlas

**Direction**:
1. Add a `## Voice Identity` section to your project's CLAUDE.md:
   ```markdown
   ## Voice Identity
   **Voice**: `am_adam`
   **Service**: http://100.123.83.34:8880/v1/audio/speech
   **Registry**: ~/ASIF/standards/portfolio-voice-registry.md
   **Use**: every cycle-complete, every P0/P1 completion, every directive response.
   ```
2. Update your `cos-speak` wrapper (or equivalent) to default to `am_adam` on your surfaces.
3. On every directive DONE / ship complete / cycle complete, speak a one-sentence summary using your voice.
4. Sample call:
   ```bash
   curl -sS -X POST http://100.123.83.34:8880/v1/audio/speech \
     -H "Content-Type: application/json" \
     -d '{"model":"kokoro","input":"Your message here.","voice":"am_adam","response_format":"wav"}' \
     -o /tmp/voice.wav && aplay /tmp/voice.wav  # or pipe to PowerShell on WSL2
   ```

**Push back allowed**: If you want a different voice, write a response in this NEXUS with the requested voice ID and reason. Registry file authoritative: `~/ASIF/standards/portfolio-voice-registry.md` — no duplicates portfolio-wide.

**Not required**: don't build a new service. Use PP's endpoint as-is. If you need streaming (long narrations, live dialogue), use `/v1/audio/speech/stream` — see PP's `docs/voice-service/user-guide.md`.

**Why P2 Saturday**: low-stakes identity work, immediate quality-of-life improvement. Won't block anything. Pick up at your next session-start.

2. Execute any PENDING directives before other work (unless Asif overrides)
3. Write your response inline under each directive
4. Update initiative statuses in NEXUS if your work changes them
5. If you have questions for the CoS, add them under `## Team Questions` in NEXUS

## Execution Strategy
For any directive that touches 3+ files or requires architectural decisions:
1. USE PLAN MODE — think before you code. Outline your approach first.
2. USE AGENT TEAMS — break complex work into parallel sub-tasks.
3. Test everything. Test counts never decrease.

---

## CoS Directives

> 1 completed directive archived. Active directives below.

### Directive Summary

| ID | Title | Status | Date |
|----|-------|--------|------|
| NXTG-20260311-01 | Test Coverage Push (30 → 221, 7.4x) | DONE | 2026-03-11 |
| NXTG-20260312-01 | PyPI Distribution Readiness | DONE | 2026-03-12 |
| NXTG-20260321-01 | PyPI Publish Prep (Emma Track 2) | PENDING | 2026-03-21 |
| NXTG-20260414-03 | P2: CI Gate Protocol Onboarding | PENDING | 2026-04-14 |

### DIRECTIVE-NXTG-20260414-03 — P2: CI Gate Protocol Onboarding
**From**: Emma (CLX9 Sr. CoS) via Wolf (NXTG-AI) | **Priority**: P2
**Injected**: 2026-04-14 21:48 PDT | **Estimate**: S | **Status**: PENDING
**Origin**: Emma HANDOFF Note 27 (2026-04-14 23:35 CDT). Audit found Atlas has no `.git/hooks/pre-push` installed — never onboarded to CI Gate Protocol.

**Context**: Per ADR-008 (CI Gate Protocol), every ASIF project pushes through a pre-push hook that runs the test suite before allowing the push. This prevents broken code from reaching origin. As of today (2026-04-14), this hook template also includes a **docs/governance-only fast path** (ADR-008 amendment, commit `af6fc303d`) that skips the test suite for pure-markdown edits — fixes a real governance gap where CoS NEXUS injects were blocked by unrelated test failures. See `~/ASIF/standards/ci-gate-protocol.md` and `~/ASIF/standards/ci-gate-protocol.md` amendments.

**Why Atlas**: You have 221 tests (good coverage) and are on PyPI publish track — adding the CI Gate makes publishes safer. Not urgent (Atlas is GREEN and stable), hence P2.

**Action Items**:
1. [ ] Install hook: `cp ~/ASIF/scripts/templates/pre-push-hook.sh .git/hooks/pre-push && chmod +x .git/hooks/pre-push`
2. [ ] Create `.asif-ci` config file at repo root with your test command (one line). Suggested: `python -m pytest --tb=short -q` (or whatever matches your current test invocation — pick what works locally today).
3. [ ] Test: make a trivial markdown-only commit (e.g., update README line) and `git push`. Output should show `=== ASIF CI Gate: docs/governance-only push — test suite skipped ===`.
4. [ ] Test: make a trivial code commit (e.g., add a comment to one `.py` file) and `git push`. Output should show the tests running, then passing, then push landing.
5. [ ] Write response in this directive when both test pushes verify.

**Constraints**:
- Do NOT install the hook without the `.asif-ci` config — it falls back to auto-detection which may misidentify your project type.
- If tests fail during step 4, that is a legitimate finding — fix the failing test OR flag it back to Wolf as a Team Question. Do not bypass with `--no-verify`.
- Use your existing test command, not a theoretical one. The hook should reflect what you actually run locally.

**Reference**: `~/ASIF/scripts/templates/pre-push-hook.sh` (source of truth), Emma HANDOFF Note 27.

**Response** (fill when verified):
> _(to be filled by team)_

---

### DIRECTIVE-NXTG-20260312-01 — PyPI Distribution Readiness
**From**: NXTG-AI CoS (Wolf) | **Priority**: P1
**Injected**: 2026-03-12 10:15 | **Estimate**: S | **Status**: DONE

**Context**: Atlas is Launch Week candidate (mid-April). N-06 (PyPI publish) is blocked on Asif's credentials, but all packaging prep can be done NOW so publish is one command when credentials arrive. 221 tests, CI GREEN — quality is high. Get distribution-ready.

**Action Items**:
1. [ ] Verify `pyproject.toml` has: proper `[project]` metadata (name=`nxtg-atlas`, version, description, license=Apache-2.0, classifiers for Python 3.11/3.12/3.13, URLs for GitHub/docs/issues).
2. [ ] Verify `[project.scripts]` entry point exists: `atlas = "atlas.cli:main"` (or equivalent). User should be able to `pip install nxtg-atlas && atlas scan .`
3. [ ] Run `python -m build` — verify sdist + wheel build without errors. Fix any build issues.
4. [ ] Run `twine check dist/*` — verify package metadata passes PyPI validation.
5. [ ] Update README.md: add PyPI badge placeholder (`![PyPI](https://img.shields.io/pypi/v/nxtg-atlas)`), installation section (`pip install nxtg-atlas`), quick-start usage section with 3-line example.
6. [ ] Run full test suite — 221 baseline must hold.
7. [ ] Report: build output, twine check result, test count, any issues found.

**Constraints**:
- Do NOT publish to PyPI — credentials aren't set up yet. Just verify the package BUILDS and VALIDATES.
- Do NOT add new features. This is packaging + README polish only.
- If `build` or `twine` are not installed, add them to dev dependencies.

**Completion Report** (2026-03-13):
1. [x] `pyproject.toml` verified: name=`nxtg-atlas`, version=0.2.0, description, license=MIT (PEP 639 expression), classifiers for 3.11/3.12/3.13, URLs for GitHub/docs/issues. Note: directive said Apache-2.0 but project is MIT everywhere (LICENSE file, README, pyproject.toml) — kept MIT.
2. [x] `[project.scripts]` has `atlas = "atlas.cli:app"` + `nxtg-atlas = "atlas.cli:app"`. `pip install nxtg-atlas && atlas scan .` will work.
3. [x] `python -m build` — sdist + wheel built clean: `nxtg_atlas-0.2.0.tar.gz` + `nxtg_atlas-0.2.0-py3-none-any.whl`
4. [x] `twine check dist/*` — PASSED for both artifacts.
5. [x] README updated: PyPI badge, Python version badge, MIT badge, tests badge added.
6. [x] Full test suite: **221 passed in 0.64s**. Baseline holds.
7. [x] License classifier note: PEP 639 (setuptools ≥68) supersedes `License ::` classifiers when `license` expression is set. `license = "MIT"` is sufficient — adding the classifier causes a build error.

**Ready to publish**: One command when Asif sets up PyPI credentials: `twine upload dist/*`

### DIRECTIVE-NXTG-20260321-01 — P1: PyPI Publish Prep (Emma Track 2)
**From**: NXTG-AI CoS (Wolf) via Emma | **Priority**: P1
**Injected**: 2026-03-21 10:30 | **Estimate**: S | **Status**: DONE

**Context**: Emma's Revenue Sprint Track 2 — Atlas needs PyPI prep so Asif can trigger publish.

**Action Items**:
1. [x] Create GitHub Action workflow for PyPI trusted publisher (auto-publish on release) — `.github/workflows/release.yml` already existed; added `environment: pypi` for trusted publisher compliance
2. [x] Verify `pip install nxtg-atlas` works cleanly — built wheel, installed in clean venv, all commands functional
3. [x] Write PyPI long_description from README — `readme = "README.md"` in pyproject.toml
4. [x] Verify CLI entry point works: `atlas --help`, `atlas version`, `nxtg-atlas version` — both entry points work
5. [x] Tests must pass before push — 2181 passed

**Constraints**:
- Run bash .git/hooks/pre-push before pushing — PASSED
- Package name: `nxtg-atlas` (already configured in pyproject.toml)

**Response** (filled by team):
All items complete. Package name is `nxtg-atlas` (already set). Fixed version command to read from correct package name. Synced `__init__.py` version to 0.2.0. Added `environment: pypi` to release workflow for trusted publisher. Build and install verified in clean venv. **Status: DONE**. Asif needs to configure Trusted Publisher on PyPI (Settings → Publishing → add GitHub Actions publisher for `nxtg-ai/repoatlas` repo, `release.yml` workflow, `publish` environment).

---

## Portfolio Intelligence

- **Formalized as P-15** (2026-03-06): Asif approved Atlas formalization. Part of Portfolio Intelligence vertical.
- **Revenue track**: Second revenue product after Faultline Pro (P-08b). Open Core vs Faultline SaaS model — different GTM.
- **ASIF dogfooding**: Atlas scans the same portfolio ASIF governs. The CLI could consume NEXUS data for richer health scoring.
- **Cognitive Bridge opportunity**: dx3-mcp (threedb P-05) Cognitive Memory Bridge could give Atlas persistent memory across scans.
- **PI-05: Content pipeline ready** (2026-03-11, Wolf): P-14 (nxtg-content-engine) has a proven 5-dimension editorial pipeline with 8 successful runs. When Atlas reaches PyPI (N-06), launch content (comparison posts, HN launch support, tutorial) can route through P-14's pipeline. Coordinate with P-14 team on publish schedule.
- **PI-06: Test coverage exemplary** (2026-03-11, Wolf): 221 tests from 30 in one session. This 7.4x increase is the fastest coverage push in portfolio history. Team quality is high — ready for distribution work (N-06, N-07, N-08).

---

## Team Questions

_(No pending questions)_

---

## Changelog

| Date | Change |
|------|--------|
| 2026-03-06 | Formalized as P-15. NEXUS created by CLX9 Sr. CoS (Emma). |
| 2026-03-04 | Product built by Wolf (NXTG-AI CoS). 1,814 LOC, 30 tests, CI GREEN. |
