response_format={
    "type": "text",
    "mime_type": "application/json",
    "schema": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "hook": {"type": "string"},
            "script": {"type": "string"},
            "scenes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "prompt": {"type": "string"}
                    },
                    "required": ["text", "prompt"]
                }
            }
        },
        "required": [
            "title",
            "hook",
            "script",
            "scenes"
        ]
    }
}
