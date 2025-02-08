import streamlit as st
import json
import os
from dotenv import load_dotenv
from typing import Dict, Any
import tempfile

from src.llm.openai_client import OpenAIClient
from src.agents.evaluation_agent import EvaluationAgent
from src.agents.summary_agent import SummaryAgent
from src.agents.feedback_agent import FeedbackAgent
from src.agents.motion_spilit_agent import MotionspilitAgent
from src.debate.debate_data import DebateData
from src.utils.data_loader import load_debate_data, load_evaluation_criteria
from src.utils.prompt_loader import load_prompt

# Page config
st.set_page_config(
    page_title="LLM Debate Judge",
    page_icon="⚖️",
    layout="wide"
)

# Title
st.title("LLM Debate Judge")
st.markdown("ディベートの自動評価システム")

# Sidebar for configurations
with st.sidebar:
    st.header("設定")
    
    # API Key input
    api_key = st.text_input("passkey", type="password")
    if not api_key:
        st.warning("Please enter your OpenAI API key")
    
    # Model selection
    model = st.selectbox(
        "モデルを選択",
        ["gpt-4o", "gpt-4o-mini"]
    )
    
    # Evaluation criteria selection
    criteria_options = {
        "標準評価基準": "data/evaluation_criteria.json",
        "簡易評価基準": "data/evaluation_criteria_test.json"
    }
    selected_criteria = st.selectbox(
        "評価基準を選択",
        list(criteria_options.keys())
    )

# Main content
st.header("ディベートデータのアップロード")

uploaded_file = st.file_uploader("JSONファイルをアップロード", type=['json'])

if uploaded_file and api_key:
    # Initialize all required paths
    evaluation_prompt_path = "data/prompts/evaluation_prompt.json"
    summary_prompt_path = "data/prompts/summary_prompt.json"
    feedback_prompt_path = "data/prompts/feedback_prompt.json"
    motion_spilit_prompt_path = "data/prompts/motion_spilit_prompt.json"
    
    # Create LLM client
    llm_client = OpenAIClient(api_key=api_key, model=model)
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        # Load debate data and evaluation criteria
        debate_data = load_debate_data(tmp_file_path)
        evaluation_criteria = load_evaluation_criteria(criteria_options[selected_criteria])
        
        # Load prompts
        evaluation_prompt = load_prompt(evaluation_prompt_path)
        summary_prompt = load_prompt(summary_prompt_path)
        feedback_prompt = load_prompt(feedback_prompt_path)
        motion_spilit_prompt = load_prompt(motion_spilit_prompt_path)
        
        # Show progress
        with st.spinner("評価を実行中..."):
            # Display debate data
            st.subheader("ディベート内容")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**議題**")
                st.write(debate_data.topic)
                st.markdown("**肯定側の主張**")
                st.write(debate_data.affirmative_argument)
            with col2:
                st.markdown("**否定側の反論**")
                st.write(debate_data.counter_argument)
                st.markdown("**肯定側の再構築**")
                st.write(debate_data.reconstruction)
            
            # Motion Split Analysis
            st.subheader("議題分析")
            motion_agent = MotionspilitAgent(llm_client, motion_spilit_prompt)
            motion_analysis = motion_agent.generate_intention(debate_data)
            st.write(motion_analysis)
            
            # Evaluation Results
            st.subheader("評価結果")
            evaluation_results = []
            
            for aspect_criteria in evaluation_criteria.criteria:
                with st.expander(f"{aspect_criteria.aspect}の評価"):
                    evaluation_agent = EvaluationAgent(llm_client, evaluation_prompt, aspect_criteria)
                    aspect_results = evaluation_agent.evaluate(debate_data)
                    
                    for result in aspect_results:
                        st.markdown(f"**{result['focus']}**")
                        st.write(result['result'])
                    
                    evaluation_results.append({
                        "aspect": aspect_criteria.aspect,
                        "result": aspect_results
                    })
            
            # Summary
            st.subheader("総括")
            summary_agent = SummaryAgent(llm_client, summary_prompt)
            summary = summary_agent.summarize(
                debate_data,
                evaluation_results,
                evaluation_criteria.criteria
            )
            st.write(summary)
            
            # Feedback
            st.subheader("フィードバック")
            feedback_agent = FeedbackAgent(llm_client, feedback_prompt)
            feedback = feedback_agent.generate_feedback(
                debate_data,
                summary,
                motion_analysis
            )
            st.write(feedback)
            
            # Download button for results
            results = {
                "debate_data": debate_data.__dict__,
                "motion_analysis": motion_analysis,
                "evaluation_results": evaluation_results,
                "summary": summary,
                "feedback": feedback
            }
            
            st.download_button(
                label="結果をダウンロード",
                data=json.dumps(results, ensure_ascii=False, indent=2),
                file_name="debate_evaluation_results.json",
                mime="application/json"
            )
        
        # Cleanup
        os.unlink(tmp_file_path)
        
    except Exception as e:
        st.error(f"エラーが発生しました: {str(e)}")
        if 'tmp_file_path' in locals():
            os.unlink(tmp_file_path)

else:
    st.info("ディベートデータをJSONファイルとしてアップロードしてください．")