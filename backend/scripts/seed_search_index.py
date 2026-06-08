"""
scripts/seed_search_index.py

Creates the Azure AI Search index with a searchable schema and uploads a
curated set of real, verified learning resources.

Run once (or whenever you change the dataset):

    cd backend
    python scripts/seed_search_index.py

Requires AZURE_SEARCH_ENDPOINT and AZURE_SEARCH_API_KEY (admin key) in .env.
The admin key — not a query key — is needed to create the index.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Allow running as `python scripts/seed_search_index.py` from backend/.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from azure.core.credentials import AzureKeyCredential  # noqa: E402
from azure.search.documents import SearchClient  # noqa: E402
from azure.search.documents.indexes import SearchIndexClient  # noqa: E402
from azure.search.documents.indexes.models import (  # noqa: E402
    SearchableField,
    SearchIndex,
    SimpleField,
    SearchFieldDataType,
)

from core.config import get_settings  # noqa: E402

# ── Index schema ───────────────────────────────────────────────────────────────
# title/description/topic are searchable so a gap concept matches on text.
# resource_type is filterable so the curator can honour resource preferences.
FIELDS = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="title", type=SearchFieldDataType.String),
    SearchableField(name="description", type=SearchFieldDataType.String),
    SearchableField(name="topic", type=SearchFieldDataType.String, filterable=True),
    SimpleField(name="url", type=SearchFieldDataType.String),
    SimpleField(
        name="resource_type",
        type=SearchFieldDataType.String,
        filterable=True,
        facetable=True,
    ),
    SimpleField(name="estimated_hours", type=SearchFieldDataType.Double),
]


# ── Curated resources (real, verified URLs on trusted domains) ─────────────────
RESOURCES = [
    # ── Cloud fundamentals ────────────────────────────────────────────────────
    {
        "id": "1",
        "title": "Microsoft Azure Fundamentals (AZ-900) Learning Path",
        "description": "Official Microsoft Learn path covering cloud concepts, "
        "core Azure services, security, pricing and support for the AZ-900 exam.",
        "topic": "cloud concepts IaaS PaaS SaaS Azure fundamentals",
        "url": "https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/",
        "resource_type": "official_docs",
        "estimated_hours": 8.0,
    },
    {
        "id": "2",
        "title": "Describe cloud computing — Microsoft Learn",
        "description": "Explains cloud service models IaaS, PaaS and SaaS, the "
        "shared responsibility model, and public/private/hybrid cloud.",
        "topic": "cloud service models IaaS PaaS SaaS shared responsibility",
        "url": "https://learn.microsoft.com/en-us/training/modules/describe-cloud-compute/",
        "resource_type": "official_docs",
        "estimated_hours": 1.5,
    },
    {
        "id": "3",
        "title": "Azure Fundamentals Certification Course (freeCodeCamp)",
        "description": "Full-length video course walking through every AZ-900 "
        "topic with hands-on demos of the Azure portal.",
        "topic": "Azure fundamentals cloud concepts certification exam prep",
        "url": "https://www.youtube.com/@freecodecamp",
        "resource_type": "video",
        "estimated_hours": 4.0,
    },
    # ── Azure architecture ────────────────────────────────────────────────────
    {
        "id": "4",
        "title": "Azure architecture and core resources — Microsoft Learn",
        "description": "Covers regions, availability zones, resource groups, "
        "Azure Resource Manager, subscriptions and management groups.",
        "topic": "Azure architecture resource manager regions availability zones",
        "url": "https://learn.microsoft.com/en-us/training/paths/azure-fundamentals-describe-azure-architecture-services/",
        "resource_type": "official_docs",
        "estimated_hours": 3.0,
    },
    {
        "id": "5",
        "title": "Azure Architecture Center",
        "description": "Reference architectures, design patterns and best "
        "practices for building solutions on Azure.",
        "topic": "Azure architecture design patterns reference architecture components",
        "url": "https://learn.microsoft.com/en-us/azure/architecture/",
        "resource_type": "article",
        "estimated_hours": 2.5,
    },
    # ── Azure security & compliance ───────────────────────────────────────────
    {
        "id": "6",
        "title": "Describe Azure identity, access and security — Microsoft Learn",
        "description": "Microsoft Entra ID, multifactor authentication, "
        "role-based access control, zero trust and defense in depth.",
        "topic": "Azure security identity access compliance RBAC zero trust",
        "url": "https://learn.microsoft.com/en-us/training/paths/describe-azure-identity-governance-privacy-compliance-features/",
        "resource_type": "official_docs",
        "estimated_hours": 3.0,
    },
    {
        "id": "7",
        "title": "Microsoft Azure Security Documentation",
        "description": "Guidance and standards for securing workloads, data "
        "protection, governance and regulatory compliance on Azure.",
        "topic": "Azure security compliance standards governance data protection",
        "url": "https://learn.microsoft.com/en-us/azure/security/",
        "resource_type": "official_docs",
        "estimated_hours": 2.0,
    },
    # ── Azure pricing & support ───────────────────────────────────────────────
    {
        "id": "8",
        "title": "Describe Azure pricing and lifecycle — Microsoft Learn",
        "description": "Azure subscriptions, cost management, total cost of "
        "ownership calculator, service-level agreements and support plans.",
        "topic": "Azure pricing cost management support SLA billing",
        "url": "https://learn.microsoft.com/en-us/training/paths/describe-azure-management-governance/",
        "resource_type": "official_docs",
        "estimated_hours": 2.5,
    },
    # ── AWS fundamentals ──────────────────────────────────────────────────────
    {
        "id": "9",
        "title": "AWS Cloud Practitioner Essentials",
        "description": "Official AWS training introducing cloud concepts, core "
        "services, security, architecture, pricing and support.",
        "topic": "AWS cloud practitioner fundamentals core services pricing",
        "url": "https://aws.amazon.com/training/",
        "resource_type": "official_docs",
        "estimated_hours": 6.0,
    },
    {
        "id": "10",
        "title": "AWS Documentation",
        "description": "Comprehensive official documentation for every AWS "
        "service, including getting-started guides and best practices.",
        "topic": "AWS services documentation cloud architecture",
        "url": "https://docs.aws.amazon.com/",
        "resource_type": "official_docs",
        "estimated_hours": 3.0,
    },
    {
        "id": "11",
        "title": "Amazon Web Services — Official YouTube Channel",
        "description": "Official AWS videos: service deep-dives, re:Invent talks "
        "and tutorials across cloud, AI and machine learning.",
        "topic": "AWS cloud AI machine learning tutorials videos",
        "url": "https://www.youtube.com/@amazonwebservices",
        "resource_type": "video",
        "estimated_hours": 3.0,
    },
    # ── Machine learning ──────────────────────────────────────────────────────
    {
        "id": "12",
        "title": "Kaggle Learn — Intro to Machine Learning",
        "description": "Hands-on, free micro-course covering supervised learning, "
        "model training, validation and evaluation metrics.",
        "topic": "machine learning fundamentals supervised unsupervised model evaluation",
        "url": "https://www.kaggle.com/learn/intro-to-machine-learning",
        "resource_type": "practice",
        "estimated_hours": 3.0,
    },
    {
        "id": "13",
        "title": "Machine Learning Crash Course — Google",
        "description": "Google's fast-paced introduction to ML concepts, "
        "including loss, gradient descent, and classification metrics.",
        "topic": "machine learning fundamentals algorithms metrics accuracy precision recall",
        "url": "https://developers.google.com/machine-learning/crash-course",
        "resource_type": "official_docs",
        "estimated_hours": 6.0,
    },
    {
        "id": "14",
        "title": "Kaggle Learn — Intermediate Machine Learning",
        "description": "Practice with missing values, categorical encoding, "
        "pipelines, cross-validation and gradient boosting.",
        "topic": "machine learning model evaluation cross validation pipelines",
        "url": "https://www.kaggle.com/learn/intermediate-machine-learning",
        "resource_type": "practice",
        "estimated_hours": 4.0,
    },
    # ── Generative & applied AI ───────────────────────────────────────────────
    {
        "id": "15",
        "title": "Microsoft AI for Beginners",
        "description": "Open-source curriculum on AI and machine learning "
        "fundamentals, including neural networks and generative models.",
        "topic": "AI fundamentals generative AI neural networks deep learning",
        "url": "https://github.com/microsoft/AI-For-Beginners",
        "resource_type": "practice",
        "estimated_hours": 10.0,
    },
    {
        "id": "16",
        "title": "Microsoft Generative AI for Beginners",
        "description": "21-lesson course covering prompt engineering, large "
        "language models, RAG and building generative AI applications.",
        "topic": "generative AI prompt engineering large language models LLM RAG",
        "url": "https://github.com/microsoft/generative-ai-for-beginners",
        "resource_type": "practice",
        "estimated_hours": 12.0,
    },
    {
        "id": "17",
        "title": "AWS Skill Builder — Generative AI",
        "description": "Official AWS learning on generative AI, Amazon Bedrock, "
        "foundation models and responsible AI practices.",
        "topic": "generative AI AWS Bedrock foundation models responsible AI",
        "url": "https://aws.amazon.com/training/",
        "resource_type": "official_docs",
        "estimated_hours": 5.0,
    },
    # ── Networking ────────────────────────────────────────────────────────────
    {
        "id": "18",
        "title": "Azure Networking Fundamentals — Microsoft Learn",
        "description": "Virtual networks, subnets, VPN gateways, load balancing "
        "and DNS in Azure.",
        "topic": "Azure networking virtual networks VPN load balancer subnets",
        "url": "https://learn.microsoft.com/en-us/training/modules/azure-networking-fundamentals/",
        "resource_type": "official_docs",
        "estimated_hours": 2.0,
    },
    # ── Python / foundations ──────────────────────────────────────────────────
    {
        "id": "19",
        "title": "Python for Everybody (freeCodeCamp)",
        "description": "Beginner-friendly full Python course — variables, data "
        "structures, functions and working with data.",
        "topic": "Python programming fundamentals data structures",
        "url": "https://www.freecodecamp.org/",
        "resource_type": "video",
        "estimated_hours": 6.0,
    },
    {
        "id": "20",
        "title": "Microsoft Learn Training Catalog",
        "description": "Searchable catalog of free, self-paced learning paths "
        "and modules across Azure, AI, data and security.",
        "topic": "Microsoft Learn training catalog Azure AI data certification",
        "url": "https://learn.microsoft.com/en-us/training/",
        "resource_type": "official_docs",
        "estimated_hours": 1.0,
    },
]


def main() -> None:
    settings = get_settings()

    if not settings.azure_search_endpoint:
        raise SystemExit("AZURE_SEARCH_ENDPOINT is not set in .env")
    if not settings.azure_search_api_key:
        raise SystemExit(
            "AZURE_SEARCH_API_KEY (admin key) is not set in .env — "
            "the admin key is required to create the index."
        )

    credential = AzureKeyCredential(settings.azure_search_api_key)
    index_name = settings.azure_search_index_name

    # 1. Create (or update) the index schema.
    index_client = SearchIndexClient(
        endpoint=settings.azure_search_endpoint, credential=credential
    )
    index = SearchIndex(name=index_name, fields=FIELDS)
    index_client.create_or_update_index(index)
    print(f"✓ Index '{index_name}' created/updated with {len(FIELDS)} fields")

    # 2. Upload the curated resources.
    search_client = SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=index_name,
        credential=credential,
    )
    result = search_client.upload_documents(documents=RESOURCES)
    succeeded = sum(1 for r in result if r.succeeded)
    print(f"✓ Uploaded {succeeded}/{len(RESOURCES)} resources")
    print("\nDone. Your index is ready — regenerate a plan to see real results.")


if __name__ == "__main__":
    main()
