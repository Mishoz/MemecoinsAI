from sentiment_analysis import main
try:
    main()
    print("Test passed")
except Exception as e:
    print("Test failed:", e)
    exit(1)