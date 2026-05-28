@echo off
echo Installing browser-use and dependencies...

python -m pip install browser-use playwright python-dotenv langchain-openai

echo Installing Playwright browsers...
python -m playwright install chromium

echo Setup complete!
