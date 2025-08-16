#!/usr/bin/env python3
"""
Manual Test Script for HuggingFace API Integration

This script tests the HuggingFace API with your actual API key to help debug
the AI grooming functionality. Run this script to see exactly what happens
when we call the HuggingFace Inference API.

Usage:
    python manual_tests/test_huggingface_api.py
"""

import os
import sys
import json
import requests
import time
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    env_path = Path(__file__).parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment from: {env_path}")
    else:
        print(f"❌ .env file not found at: {env_path}")
        print("Please create a .env file with your HuggingFace API key")
        sys.exit(1)
        
except ImportError:
    print("❌ python-dotenv not installed. Run: pip install python-dotenv")
    sys.exit(1)


def test_api_key_validity():
    """Test if the HuggingFace API key is valid."""
    api_key = os.getenv('HF_API_KEY')
    
    if not api_key:
        print("❌ HF_API_KEY not found in environment variables")
        print("Please add your HuggingFace API key to the .env file:")
        print("HF_API_KEY=your_actual_key_here")
        return False
    
    print(f"🔑 Using API key: {api_key[:10]}...{api_key[-4:]}")
    
    # Test API key with whoami endpoint
    headers = {'Authorization': f'Bearer {api_key}'}
    
    try:
        print("\n🔍 Testing API key validity...")
        response = requests.get(
            'https://huggingface.co/api/whoami',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ API key is valid! User: {user_info.get('name', 'unknown')}")
            return True
        else:
            print(f"❌ API key validation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.RequestException as e:
        print(f"❌ Error testing API key: {e}")
        return False


def test_inference_api():
    """Test the HuggingFace Inference API with different models."""
    api_key = os.getenv('HF_API_KEY')
    
    # List of models to try (from most preferred to fallback options)
    models_to_try = [
        {
            'name': 'mistralai/Mistral-7B-Instruct-v0.2',
            'description': 'Mistral 7B (preferred for todo grooming)'
        },
        {
            'name': 'microsoft/DialoGPT-medium', 
            'description': 'DialoGPT Medium (conversational)'
        },
        {
            'name': 'facebook/blenderbot-400M-distill',
            'description': 'BlenderBot (chatbot)'
        },
        {
            'name': 'gpt2',
            'description': 'GPT-2 (basic text generation)'
        }
    ]
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    # Test prompt similar to what we use for todo grooming
    test_prompt = """You are an AI assistant specialized in organizing todo lists. Please improve this todo list:

buy milk
get groceries
buy milk
walk dog
do important stuff

Please respond with a JSON object containing:
{
    "groomed_tasks": [
        {"title": "Clear task description", "priority": "high|medium|low"}
    ],
    "processing_notes": "What changes were made"
}"""

    print(f"\n🧪 Test prompt:\n{'-'*50}")
    print(test_prompt[:200] + "..." if len(test_prompt) > 200 else test_prompt)
    print(f"{'-'*50}\n")
    
    for model_info in models_to_try:
        model_name = model_info['name']
        description = model_info['description']
        
        print(f"🤖 Testing model: {model_name}")
        print(f"   Description: {description}")
        
        url = f"https://api-inference.huggingface.co/models/{model_name}"
        
        payload = {
            "inputs": test_prompt,
            "parameters": {
                "max_new_tokens": 500,
                "temperature": 0.3,
                "do_sample": True,
                "return_full_text": False
            }
        }
        
        try:
            print(f"   📡 Making API call to: {url}")
            
            start_time = time.time()
            response = requests.post(
                url, 
                headers=headers, 
                json=payload,
                timeout=30
            )
            duration = time.time() - start_time
            
            print(f"   ⏱️  Response time: {duration:.2f}s")
            print(f"   📊 Status code: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"   ✅ SUCCESS! Model is working")
                    print(f"   📝 Response type: {type(result)}")
                    
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get('generated_text', str(result[0]))
                        print(f"   📄 Generated text (first 300 chars):")
                        print(f"   {generated_text[:300]}...")
                    else:
                        print(f"   📄 Raw response: {str(result)[:300]}...")
                    
                    print(f"   🎉 RECOMMENDED: Use {model_name} for AI grooming!")
                    return model_name
                    
                except json.JSONDecodeError:
                    print(f"   ⚠️  Response not JSON: {response.text[:200]}...")
                    
            elif response.status_code == 503:
                print(f"   ⏳ Model is loading... (this is normal for cold starts)")
                print(f"   💡 Try again in 20-30 seconds")
                
            elif response.status_code == 401:
                print(f"   ❌ Unauthorized - check your API key")
                
            elif response.status_code == 404:
                print(f"   ❌ Model not found or not available")
                
            elif response.status_code == 429:
                print(f"   ⚠️  Rate limited - too many requests")
                
            else:
                print(f"   ❌ Error: {response.text[:200]}")
                
        except requests.RequestException as e:
            print(f"   ❌ Request error: {e}")
        
        print()  # Empty line between models
    
    print("❌ No working models found. Check your API key or try again later.")
    return None


def test_our_grooming_service():
    """Test our actual grooming service implementation."""
    try:
        from ai.grooming_service import GroomingService
        
        print("🔬 Testing our GroomingService implementation...")
        
        service = GroomingService()
        print(f"   Primary service: {service.config.primary_service}")
        print(f"   Has HF key: {service.config.has_hf_key}")
        
        test_input = """
        buy milk
        get groceries
        buy milk again
        walk the dog
        do something urgent and important
        maybe clean house
        """
        
        print(f"   📝 Test input: {test_input.strip()}")
        print("   🚀 Calling grooming service...")
        
        result = service.groom_todo_list(test_input)
        
        print(f"   📊 Result:")
        print(f"      Success: {result.success}")
        print(f"      Fallback used: {result.fallback_used}")
        print(f"      Tasks found: {len(result.groomed_tasks)}")
        print(f"      Error: {result.error_message}")
        
        if result.groomed_tasks:
            print(f"   📋 Formatted output:")
            formatted = result.get_formatted_tasks()
            for line in formatted.split('\n')[:5]:  # First 5 lines
                print(f"      {line}")
        
        if result.processing_notes:
            print(f"   📝 Notes: {result.processing_notes}")
            
        return result.success and not result.fallback_used
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False


def main():
    """Run all manual tests."""
    print("🧪 HuggingFace API Manual Test Script")
    print("="*50)
    
    # Step 1: Test API key
    if not test_api_key_validity():
        print("\n❌ API key test failed. Please fix your API key before continuing.")
        return
    
    # Step 2: Test inference API
    working_model = test_inference_api()
    
    # Step 3: Test our service
    print("🔬 Testing Our Implementation")
    print("="*30)
    our_service_works = test_our_grooming_service()
    
    # Summary
    print("\n📊 SUMMARY")
    print("="*20)
    print(f"✅ API Key Valid: Yes")
    print(f"{'✅' if working_model else '❌'} Working Model Found: {working_model or 'None'}")
    print(f"{'✅' if our_service_works else '❌'} Our Service Works: {'Yes' if our_service_works else 'No (using fallback)'}")
    
    if working_model and not our_service_works:
        print("\n💡 RECOMMENDATION:")
        print(f"   Update your AI config to use: {working_model}")
        print(f"   Edit src/ai/config.py and change self.hf_model = '{working_model}'")
    elif not working_model:
        print("\n💡 RECOMMENDATION:")
        print("   1. Verify your HuggingFace API key at: https://huggingface.co/settings/tokens")
        print("   2. Try again later (models may be temporarily unavailable)")
        print("   3. The fallback grooming still works perfectly!")
    else:
        print("\n🎉 Everything is working! AI grooming should work in the app.")


if __name__ == '__main__':
    main()