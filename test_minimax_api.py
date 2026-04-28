#!/usr/bin/env python
"""
MiniMax API Key 测试脚本
"""
import httpx
import json
import sys

MINIMAX_API_KEY = "sk-cp-0lJKWK60XX7GOFbQA5dmo7bXKfjLnb5SslBbWRipE_GjkVtK-EiImkfXqR-dszI28CGtbHmbj149c_A2xwskTM4ZmYreseISl5a_rCGFi4HgvtM_MH1jD2c"

def test_api():
    """测试 MiniMax API Key"""
    print("=" * 50)
    print("MiniMax API Key 测试")
    print("=" * 50)
    print(f"Key: {MINIMAX_API_KEY[:20]}...{MINIMAX_API_KEY[-10:]}")
    print()

    # 尝试不同的端点和参数组合
    endpoints = [
        ("https://api.minimax.io/v1/text/chatcompletion_pro", "abab6.5s-chat"),
        ("https://api.minimax.io/v1/text/chatcompletion_v2", "abab6.5s-chat"),
        ("https://api.minimax.io/v1/text/chatcompletion_pro", "abab5.5s"),
        ("https://api.minimax.io/v1/text/chatcompletion_v2", "MiniMax-Text-01"),
    ]

    for url, model in endpoints:
        print(f"\n测试端点: {url}")
        print(f"模型: {model}")

        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一个友好的助手，用一句话回应"},
                {"role": "user", "content": "你好，请介绍自己"}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=headers, json=payload)
                print(f"状态码: {response.status_code}")

                data = response.json()
                print(f"响应: {json.dumps(data, ensure_ascii=False)[:300]}")

                # 检查是否有有效的响应
                if response.status_code == 200:
                    base_resp = data.get("base_resp", {})
                    if base_resp.get("status_code") == 0:
                        print("✅ API Key 有效!")
                        choices = data.get("choices", [])
                        if choices:
                            content = choices[0].get("message", {}).get("content", "")
                            print(f"AI回复: {content}")
                        return True
                    else:
                        print(f"❌ API返回错误: {base_resp.get('status_msg')}")
                else:
                    print(f"❌ HTTP错误: {response.status_code}")

        except Exception as e:
            print(f"❌ 请求异常: {e}")

    print("\n" + "=" * 50)
    print("所有端点测试失败")
    print("=" * 50)
    return False

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
