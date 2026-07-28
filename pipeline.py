from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipeline(topic:str)->dict:
    state = {}
    #search agent working
    print("\n"+"="*50)
    print("Step 1 - Search Agent is working")
    print("\n"+"="*50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages":[("user",f"Find recent, reliable and detailed infromation about: {topic}")],
    })
    state["search_results"] = search_result["messages"][-1].content

    print("\n serach result ", state['search_results'])

    # Step 2 - Reader Agent
    print("\n"+"="*50)
    print("Step 2 - Reader Agent is scraping top resources...")
    print("\n"+"="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages":[(
            "user",
            f"Based on the following serach results about '{topic},"
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results: \n{state['search_results'][:800]}"
        )]
    })
    state['scraped_content'] = reader_result['messages'][-1].content
    print("\n Scraped Content \n", state['scraped_content'])

    # Step 3 - Writer Chain
    print("\n"+"="*50)
    print("Step 3 - Writer is drafting the report...")
    print("\n"+"="*50)

    research_combined = (
        f"SEARCH RESULTS: \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT: \n {state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })
    print("\n Final Report \n", state['report'])

    # Critic Report
    print("\n"+"="*50)
    print("Step 4 - Critic is reviewing...")
    print("\n"+"="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state["report"]
    })
    print("\n Critic Report \n", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic: ")
    run_research_pipeline()
