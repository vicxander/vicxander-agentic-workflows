"""Check preserved neutral semantic clauses."""
try:
    from tools.validate_workflows import main
except ImportError:
    from validate_workflows import main
if __name__ == '__main__': raise SystemExit(main())
