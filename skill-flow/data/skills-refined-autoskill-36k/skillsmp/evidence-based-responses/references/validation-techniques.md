# Validation Techniques

This document describes how to verify technical claims before making them in code reviews or discussions.

## Language and Framework Behavior

When claiming that a language or framework behaves a certain way, start with official documentation. For Ruby, the primary sources are the Ruby documentation at ruby-doc.org and the Rails guides at guides.rubyonrails.org. For other languages, find the equivalent authoritative source.

If documentation is unclear or doesn't cover your specific case, write a small test to confirm the behavior. This is especially useful for edge cases or surprising behavior. You can mention in your response that you verified by testing: "I confirmed this by testing in a Rails console" adds credibility.

For framework-specific behavior like Rails autoloading, ActiveRecord callbacks, or lifecycle hooks, the Rails guides often have dedicated sections explaining the nuances. Search for keywords like "gotchas", "caveats", or "important" to find relevant warnings.

## Codebase Behavior

When claiming that existing code works a certain way, link to the source. Use grep or your editor's search to find all usages of a method, constant, or class. This helps you understand the full picture before making claims.

Read the implementation, not just the interface. If you're claiming that a method handles a certain case, look at the actual code to verify. Method names and documentation can be misleading or outdated.

Check the tests for the code in question. Tests often document expected behavior more reliably than comments, and they reveal edge cases the original author considered. If a test expects certain behavior, that's strong evidence of how the code is supposed to work.

When referencing code, use permalink URLs that include the commit SHA. This ensures your links remain valid even after the code changes. The format is: `https://github.com/org/repo/blob/<commit-sha>/path/to/file.rb#L42` for a specific line, or `#L42-L50` for a range.

## System Architecture

For claims about how systems work together (data flow, persistence, caching), trace the path through the code. Start from the entry point and follow the calls until you find the backing store, external service, or final destination.

When investigating persistence, look for database tables, Redis keys, file paths, or external API calls. Check for TTLs, expiration settings, or cleanup jobs that might affect data retention. The absence of a TTL often means data persists indefinitely, but verify this in the library documentation.

For caching behavior, find where caches are written and read. Look for invalidation logic and understand what triggers cache updates. Check if there's a version number or cache key that changes when the underlying data changes.

Document your findings with links to the relevant code. If you traced through multiple files to understand the flow, mention the key files so others can follow your reasoning.

## When Uncertain

If you cannot find definitive evidence for a claim, be explicit about the uncertainty. Phrases like "I believe this works because..." or "Based on my reading of the code..." signal that you've done research but aren't completely certain.

Ask clarifying questions rather than making uncertain assertions. "Is this designed to handle X?" is better than "This doesn't handle X" when you're not sure.

When the stakes are high (the claim affects correctness, security, or data integrity), take extra time to verify. Run the code, write a test, or ask someone with more context. It's better to delay a response than to confidently assert something incorrect.
