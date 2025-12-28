# Simple test to verify the CustomEmbeddings __call__ method
import torch
from transformers import AutoTokenizer, AutoModel

# Copy the CustomEmbeddings class with the __call__ method
class CustomEmbeddings:
    def __init__(self, model_path):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")
        # Just initialize without loading a real model to test the structure
        self.tokenizer = None
        self.model = None
        self.model_path = model_path
    
    def embed_documents(self, texts):
        return [self.embed_query(text) for text in texts]
    
    def embed_query(self, text):
        # Return dummy embeddings for testing
        return [0.1, 0.2, 0.3, 0.4, 0.5]
    
    def __call__(self, text):
        # Test the __call__ method
        print(f"__call__ method called with text: '{text}'")
        return self.embed_query(text)

# Test the class
print("Testing CustomEmbeddings class...")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

# Create an instance
embeddings = CustomEmbeddings("dummy_model_path")

# Test 1: Check if embeddings object is callable
print(f"\n1. Is embeddings object callable? {callable(embeddings)}")

# Test 2: Test the __call__ method
try:
    result = embeddings("这是一个测试文本")
    print(f"2. __call__ method works! Result: {result}")
except Exception as e:
    print(f"2. __call__ method failed: {e}")

# Test 3: Test embed_query directly
try:
    result2 = embeddings.embed_query("直接调用embed_query方法")
    print(f"3. embed_query method works! Result: {result2}")
except Exception as e:
    print(f"3. embed_query method failed: {e}")

print("\nAll tests completed!")
