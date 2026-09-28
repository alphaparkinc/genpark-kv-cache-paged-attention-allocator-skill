import sys, json
from client import PagedKVCacheAllocator

manager = PagedKVCacheAllocator()

def handle_jsonrpc(line):
    global manager
    try:
        req = json.loads(line)
        req_id = req.get("id")
        method = req.get("method")
        if method == "initialize":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "genpark-kv-cache-paged-attention-allocator-skill", "version": "1.0.0"}, "capabilities": {"tools": {}}}}
        elif method == "tools/list":
            return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
                {"name": "allocate_kv_blocks", "description": "Allocate KV blocks for sequence.", "inputSchema": {"type": "object", "properties": {"seq_id": {"type": "string"}, "num_tokens": {"type": "integer"}}, "required": ["seq_id", "num_tokens"]}},
                {"name": "free_kv_blocks", "description": "Free blocks allocated to sequence.", "inputSchema": {"type": "object", "properties": {"seq_id": {"type": "string"}}, "required": ["seq_id"]}},
                {"name": "benchmark_allocation", "description": "Run allocation benchmark.", "inputSchema": {"type": "object", "properties": {}}}
            ]}}
        elif method == "tools/call":
            params = req.get("params", {})
            tool = params.get("name")
            args = params.get("arguments", {})
            if tool == "allocate_kv_blocks":
                res = manager.allocate(args.get("seq_id", "default"), args.get("num_tokens", 16))
            elif tool == "free_kv_blocks":
                res = manager.free(args.get("seq_id", "default"))
            elif tool == "benchmark_allocation":
                res = manager.benchmark_allocation()
            else:
                return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        return {"jsonrpc": "2.0", "id": req_id, "result": {}}
    except Exception as e:
        return {"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(e)}}

def main():
    for line in sys.stdin:
        if line.strip():
            print(json.dumps(handle_jsonrpc(line.strip())), flush=True)

if __name__ == "__main__":
    main()
