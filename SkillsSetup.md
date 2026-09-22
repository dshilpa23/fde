***BMAD Setup for Project ****
set BMAD skills for project: npx bmad-method install --yes --modules bmm,bmb --all-next --tools claude-code,codex

Installation step: npm config set registry https://centraluhg.jfrog.io/artifactory/api/npm/glb-npm-remote-rem/
check packages : https://centraluhg.jfrog.io/ui/packages
npm login --auth-type=web
npx bmad-method install
or
npm install bmad-method@6.11.0 --registry https://centraluhg.jfrog.io/artifactory/api/npm/glb-npm-remote-rem/

***GRAPHYPY****
open agent and call below
graphify .


Generate API key :
https://platform.openai.com/api-keys


read -s "OPENAI_API_KEY?Paste OpenAI API key: "
export OPENAI_API_KEY
graphify extract . --backend openai

read -s "OPENAI_API_KEY?Paste OpenAI API key: "
export OPENAI_API_KEY
graphify extract . --backend openai

***Archipy***
In Chat: Prompt:npx skills add tt-a1i/archify -g
Agent Response: Installed archify globally for Codex at ~/.agents/skills/archify.

In Project: Open Agent --> Prompt:Use the archify skill to create an interactive architecture diagram of my application.
/Users/shilpa.vangati@optum.com/Library/CloudStorage/OneDrive-UHG/Desktop/AI Ref Docs/FDE/Session 03 hands-on Labs and Handouts/session3-bmad-incomplete-project/graphify-out/referral-routing-architecture.html

Use: Knowledge Graph: swimlane process flow for understanding
