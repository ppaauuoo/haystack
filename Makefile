.PHONY: browser start-mcp stop-mcp

# Start MCP server in background
start-mcp:
	@echo "Starting MCP server on port 8931..."
	npx @playwright/mcp@latest --headless --isolated --no-sandbox --port 8931 &

# Run browser.py (requires MCP server to be running)
browser:
	@echo "Running browser.py..."
	python browser.py

# Stop MCP server
stop-mcp:
	@echo "Stopping MCP server..."
	pkill -f "npx @playwright/mcp@latest"

# Clean up both processes
clean: stop-mcp
	@echo "Cleaned up processes"
