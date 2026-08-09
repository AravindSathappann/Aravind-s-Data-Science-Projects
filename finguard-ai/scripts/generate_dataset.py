import random
import pandas as pd

random.seed(42)

CLEAR_PER_CLASS = 70
AMBIGUOUS_PER_CLASS = 20
MIXED_PER_CLASS = 10

starts = [
    "Customer: Hi, ",
    "Customer: Hello, ",
    "Customer: I'm calling because ",
    "Customer: I need help because ",
]

neutral_details = [
    "I noticed this while checking the app",
    "I want to understand what the next step should be",
    "I would appreciate some guidance",
    "I just want to make sure this is handled correctly",
    "I have the account open in front of me",
]

agent_replies = [
    "Agent: Let me review that with you.",
    "Agent: I can check the account details.",
    "Agent: Let me determine the appropriate next step.",
    "Agent: I can help route this request correctly.",
]


clear = {

"Fraud Risk": [
    "I do not recognize this card purchase",
    "I did not authorize this transfer",
    "this cash withdrawal was not mine",
    "I never placed this online order",
    "someone used my card without my permission",
    "I did not send money to this recipient",
    "I was not in the city where this purchase happened",
    "these small charges do not belong to me",
],

"Compliance Risk": [
    "I want to bypass the identity verification",
    "I do not want to provide the requested ID",
    "I want the source-of-funds requirement waived",
    "I want to send this wire without the required documents",
    "I am moving money for another person and do not want to explain it",
    "I want the verification hold removed without completing the review",
    "I want to use someone else's identification for this request",
    "I want to split the transfer to avoid the documentation step",
],

"Escalation Risk": [
    "this is my fourth call and the issue is still unresolved",
    "I need a supervisor because previous agents did not fix this",
    "I was promised a callback but nobody contacted me",
    "I submitted the documents twice and the case is still pending",
    "I keep getting transferred without a solution",
    "the case has been open for weeks despite repeated follow-ups",
    "I need someone senior to take over this unresolved case",
    "I was told this would already be fixed",
],

"Normal Support": [
    "I want to know when my debit card will arrive",
    "I need help updating my mailing address",
    "I want an explanation of this monthly service fee",
    "I need to reset my online banking password",
    "I want to know my transfer limit",
    "I want to download an older statement",
    "I want to know the normal refund timeline",
    "I want to update my paperless statement settings",
]

}


ambiguous = {

"Fraud Risk": [
    "I recognize the merchant name, but I did not make this particular purchase",
    "the earlier fee question was normal, but this new charge is not mine",
    "I completed verification already, but this transfer was never submitted by me",
    "I am frustrated, but the main problem is a payment I never approved",
    "I called before about another issue, but today I found a transaction I did not make",
    "I know the recipient, but I did not initiate this particular transfer",
    "I still have my card, yet this ATM withdrawal was not made by me",
    "I thought it was a subscription, but the merchant says I have no account",
],

"Compliance Risk": [
    "I recognize every transaction, but I want the wire released without uploading my ID",
    "I am frustrated, but I still do not want to provide the requested documents",
    "I am not reporting fraud; I want the bank to skip verification while I am traveling",
    "I want to split the transfer so I can avoid submitting the documentation",
    "I have not completed identity verification but want the restriction removed",
    "I know the transfer is mine but do not want to provide source-of-funds information",
    "I am not disputing a charge; I want an exception to the verification rule",
    "I understand the policy but want the agent to override the documentation requirement",
],

"Escalation Risk": [
    "the unauthorized charge was already disputed, but nobody has updated the case after several calls",
    "I completed verification two weeks ago and the account is still restricted after three calls",
    "I recognize the transaction, but the promised correction still has not happened",
    "I submitted all required documents and need a manager because the review is stuck",
    "the fraud issue was handled, but this is now my fifth call about the account problem",
    "I understand why the transfer was held, but support promised a review days ago",
    "I am not disputing a new transaction; the existing case has gone nowhere",
    "I completed the verification rule already, but the repeated delay needs escalation",
],

"Normal Support": [
    "I recognize this charge and only want to know why it is still pending",
    "the app asked me to verify my identity and I just need directions for doing it",
    "I received a replacement card after an old fraud case and only need help activating it",
    "I want to understand the transfer limit before sending money to my own savings account",
    "the refund is pending, but I only want to know the normal processing time",
    "I noticed a service charge but I am not saying it was unauthorized",
    "I recognize the cash withdrawal and only want to know where the ATM was located",
    "I am asking about verification requirements before deciding whether to make a transfer",
]

}


mixed = {

"Fraud Risk": [
    "I called twice about verification before, but that was resolved; today I found a new charge I did not make",
    "I am frustrated with support, but the current issue is a transfer I never authorized",
    "I spoke with a manager yesterday and then another purchase appeared that was not mine",
    "I completed all verification requirements, but now there is a withdrawal I did not make",
    "I recognize an old pending charge, but the new transaction beside it is not mine",
],

"Compliance Risk": [
    "I had an unauthorized charge last month, but today I want a wire processed without providing ID",
    "I have called several times, but I still do not want to submit the required transfer documents",
    "I spoke with a manager about a fee, but now I want the bank to waive identity verification",
    "nothing appears stolen, but I want to send money for someone else without providing more information",
    "I had a card issue before, but today I am asking to bypass the source-of-funds review",
],

"Escalation Risk": [
    "I had an unauthorized charge and completed verification, but I have now called four times and the case remains unresolved",
    "I recognize the transfer and submitted the documents, but I need a supervisor because nobody has acted",
    "I am not asking to bypass policy or report new fraud; I need escalation after repeated failed support attempts",
    "I received the replacement card, but after several calls the account is still locked",
    "I understand the fee and verification rules, but the promised correction never happened",
],

"Normal Support": [
    "I had a fraud case last month and spoke with a manager, but it is resolved and today I only need to update my address",
    "I completed verification and a transfer earlier this week and only want to know when my card arrives",
    "I recognize all charges and do not need escalation; I only want to reset my password",
    "I previously disputed a transaction, but that case is closed and I just want to download a statement",
    "I talked with a supervisor about another issue before, but today I only need the normal refund timeline",
]

}


def make_examples(label):
    examples = set()

    while len(examples) < CLEAR_PER_CLASS:
        text = (
            random.choice(starts)
            + random.choice(clear[label])
            + ". "
            + random.choice(neutral_details)
            + ". "
            + random.choice(agent_replies)
        )

        examples.add(text)

    while len(examples) < CLEAR_PER_CLASS + AMBIGUOUS_PER_CLASS:
        text = (
            random.choice(starts)
            + random.choice(ambiguous[label])
            + ". "
            + random.choice(neutral_details)
            + ". "
            + random.choice(agent_replies)
        )

        examples.add(text)

    while len(examples) < CLEAR_PER_CLASS + AMBIGUOUS_PER_CLASS + MIXED_PER_CLASS:
        text = (
            random.choice(starts)
            + random.choice(mixed[label])
            + ". "
            + random.choice(neutral_details)
            + ". "
            + random.choice(agent_replies)
        )

        examples.add(text)

    return [(text, label) for text in examples]


rows = []

for label in [
    "Fraud Risk",
    "Compliance Risk",
    "Escalation Risk",
    "Normal Support"
]:
    rows.extend(make_examples(label))


random.shuffle(rows)

df = pd.DataFrame(
    rows,
    columns=["transcript", "label"]
)

assert len(df) == 400
assert df["transcript"].nunique() == 400

df.to_csv(
    "data/labeled_calls_expanded.csv",
    index=False
)

print("New harder dataset created!")
print("Total transcripts:", len(df))
print()
print(df["label"].value_counts())
