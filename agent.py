from dotenv import load_dotenv
import os
load_dotenv(".env")


from strands import Agent
from strands.models import BedrockModel
from strands_tools import python_repl, slack


bedrock_model = BedrockModel(
    model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
    region_name='ap-northeast-2',
    temperature=0,
)

agent = Agent(
    model=bedrock_model,
    tools=[python_repl, slack],
    system_prompt="""You are a FinOps specialist. When analyzing cloud costs and optimizing spend:
1. Assess Cost Drivers and Usage Patterns
   - Identify major services and resources driving spend
   - Highlight under-utilized or idle capacity
2. Recommend Optimization Actions
   - Suggest rightsizing, autoscaling, instance reservations, and savings plans
   - Advise on storage tiering, networking, and license optimization
3. Provide Budgeting, Forecasting, and Reporting
   - Create clear monthly/quarterly spend forecasts
   - Define meaningful budgets, alerts, and KPIs (e.g., cost per workload)
4. Ensure Governance and Best Practices
   - Enforce tagging strategies and cost allocation
   - Recommend policies for resource lifecycle and automated cleanup
5. Format and Delivery
   - Use Markdown with code blocks, tables, and diagrams where helpful
   - Include a concise executive summary and a detailed breakdown
   - Provide a usage example or template (e.g., Terraform snippet for tagging)
   
SECURITY CONSTRAINTS:
- Never output actual cloud credentials, API keys, or secrets
- Do not recommend overly permissive IAM roles or policies
- Always enforce the principle of least privilege
- Flag any security-sensitive configurations (e.g., public storage buckets)
- Recommend input validation for cost inputs and API parameters"""
)


msg="""
1. costsummary.pdf 파일을 심층분석해서 Insights와 Recommendations을 항목별로 자세하게 영문으로 정리해서 output/tmp_result.pdf 파일에 저장해줘.
2. 정리한 내용을 costsummary.pdf 파일과 output/tmp_result.pdf 파일을 합쳐서 output/result.pdf 파일로 저장해줘.
"""
agent(msg)

result = agent.tool.slack(
    action="files_upload_v2",
    parameters={
        "channel": "C091LHTUUKS",
        "file": "output/result.pdf"
    }
)

print("FINISHED")