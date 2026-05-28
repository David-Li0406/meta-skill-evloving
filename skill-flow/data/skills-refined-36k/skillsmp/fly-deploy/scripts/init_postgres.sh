#!/bin/bash

# Initialize and attach Postgres database to fly.io app
# Usage: ./init_postgres.sh [--app APP_NAME] [--db-name DB_NAME] [--region REGION]

set -e

APP_NAME=""
DB_NAME=""
REGION="ord"
CONFIG="development"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --app)
      APP_NAME="$2"
      shift 2
      ;;
    --db-name)
      DB_NAME="$2"
      shift 2
      ;;
    --region)
      REGION="$2"
      shift 2
      ;;
    --production)
      CONFIG="production"
      shift
      ;;
    *)
      echo "Unknown option: $1"
      echo "Usage: $0 --app APP_NAME [--db-name DB_NAME] [--region REGION] [--production]"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [ -z "$APP_NAME" ]; then
  echo "Error: --app APP_NAME is required"
  echo "Usage: $0 --app APP_NAME [--db-name DB_NAME] [--region REGION] [--production]"
  exit 1
fi

# Set default DB name if not provided
if [ -z "$DB_NAME" ]; then
  DB_NAME="${APP_NAME}-db"
fi

echo "🗄️  Setting up Postgres database for fly.io app"
echo "   App: $APP_NAME"
echo "   Database: $DB_NAME"
echo "   Region: $REGION"
echo "   Configuration: $CONFIG"
echo ""

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
  echo "❌ flyctl is not installed"
  echo "   Install: https://fly.io/docs/flyctl/install/"
  exit 1
fi

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
  echo "❌ Not logged in to fly.io"
  echo "   Run: flyctl auth login"
  exit 1
fi

# Check if app exists
if ! flyctl status -a "$APP_NAME" &> /dev/null; then
  echo "❌ App '$APP_NAME' does not exist"
  echo "   Create it first with: flyctl launch"
  exit 1
fi

# Create Postgres cluster
echo "📦 Creating Postgres cluster..."
echo ""

if [ "$CONFIG" == "production" ]; then
  echo "Creating production configuration (high availability)"
  flyctl postgres create --name "$DB_NAME" --region "$REGION"
else
  echo "Creating development configuration (single instance)"
  flyctl postgres create --name "$DB_NAME" --region "$REGION" --initial-cluster-size 1
fi

echo ""
echo "⏳ Waiting for database to be ready..."
sleep 5

# Attach database to app
echo "🔗 Attaching database to app..."
flyctl postgres attach "$DB_NAME" -a "$APP_NAME"

echo ""
echo "✅ Database setup complete!"
echo ""
echo "📋 Connection details:"
echo "   - DATABASE_URL secret has been set on your app"
echo "   - Database name: ${APP_NAME}"
echo "   - Connection string format: postgres://user:pass@${DB_NAME}.internal:5432/${APP_NAME}"
echo ""
echo "🔍 Useful commands:"
echo "   - Connect to database: flyctl postgres connect -a $DB_NAME"
echo "   - List databases: flyctl postgres db list -a $DB_NAME"
echo "   - View database logs: flyctl logs -a $DB_NAME"
echo "   - Check database status: flyctl status -a $DB_NAME"
echo ""
echo "📚 For migration setup, see: references/data-persistence.md"
