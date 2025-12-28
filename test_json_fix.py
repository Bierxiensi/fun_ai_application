# Test script to verify the JSON parsing fix
import json
import re

# Simulate the problematic response from the model
problematic_response = """
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
用户输入：客户经理被投诉了，投诉一次扣多少分 
{
    "query_type": "rag_query",
    "intent": "客户经理被投诉了，投诉一次扣多少分",
    "confidence": 0.9999999809265137,
    "reason": "根据公司规定，客户经理被投诉一次扣1分。"
}
"""

query = "客户经理被投诉了，投诉一次扣多少分"

print("Testing JSON parsing fix...")
print("Original problematic response:")
print(problematic_response[:300] + "...")
print(f"\nTotal length: {len(problematic_response)} characters")

# Apply the improved fix
try:
    # 1. Clean response: remove repeated user input
    # Find the last occurrence of the user input
    last_query_pos = problematic_response.rfind(query)
    if last_query_pos != -1:
        # From after the last user input, find the start of JSON
        json_start_pos = problematic_response.find('{', last_query_pos + len(query))
        if json_start_pos != -1:
            # Extract from JSON start position
            cleaned_response = problematic_response[json_start_pos:]
        else:
            # If no { found, extract from after last user input
            cleaned_response = problematic_response[last_query_pos + len(query):]
    else:
        cleaned_response = problematic_response
    
    print(f"\n1. After removing repeated input:")
    print(cleaned_response[:200] + "...")
    
    # 2. Remove leading/trailing whitespace and newlines
    cleaned_response = cleaned_response.strip()
    
    print(f"\n2. After stripping whitespace:")
    print(cleaned_response[:200] + "...")
    
    # 3. Find all JSON objects
    brace_positions = []
    for i, char in enumerate(cleaned_response):
        if char == '{':
            brace_positions.append(i)
    
    valid_results = []
    
    # 4. Try to parse each JSON object
    for start_idx in brace_positions:
        # Find matching closing brace
        brace_count = 1
        end_idx = start_idx + 1
        
        while end_idx < len(cleaned_response) and brace_count > 0:
            if cleaned_response[end_idx] == '{':
                brace_count += 1
            elif cleaned_response[end_idx] == '}':
                brace_count -= 1
            end_idx += 1
        
        if brace_count == 0:
            # Found a complete JSON object
            json_str = cleaned_response[start_idx:end_idx]
            try:
                result = json.loads(json_str)
                # Validate required fields
                if all(key in result for key in ['query_type', 'intent', 'confidence', 'reason']):
                    valid_results.append(result)
                    print(f"\n✓ Found valid JSON object:")
                    print(f"  Query type: {result['query_type']}")
                    print(f"  Intent: {result['intent']}")
                    print(f"  Confidence: {result['confidence']}")
                    print(f"  Reason: {result['reason']}")
            except Exception as e:
                print(f"\n✗ Failed to parse JSON: {e}")
                print(f"  JSON string: {json_str[:100]}...")
    
    if not valid_results:
        # 5. Try regex approach for more aggressive extraction
        print(f"\n3. Trying regex approach...")
        json_pattern = r'\{[\s\S]*?\}'
        json_matches = re.findall(json_pattern, cleaned_response)
        
        for json_str in json_matches:
            try:
                result = json.loads(json_str)
                if all(key in result for key in ['query_type', 'intent', 'confidence', 'reason']):
                    valid_results.append(result)
                    print(f"✓ Found valid JSON via regex:")
                    print(f"  Query type: {result['query_type']}")
                    print(f"  Intent: {result['intent']}")
                    break
            except:
                continue
    
    print(f"\nFinal results:")
    print(f"- Valid JSON objects found: {len(valid_results)}")
    if valid_results:
        print(f"- Successfully extracted JSON from problematic response!")
    else:
        print(f"- Failed to extract valid JSON")
        
except Exception as e:
    print(f"\nError during test: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed!")
