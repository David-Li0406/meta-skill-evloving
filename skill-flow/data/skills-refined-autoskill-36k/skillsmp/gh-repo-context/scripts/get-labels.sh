#!/bin/bash
# Get available labels for current repo

gh label list --json name,description,color
