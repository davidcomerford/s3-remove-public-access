import boto3
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich import print
from rich.progress import track

s3_client = ""

def set_colour(setting):
    if setting == False:
        setting = "[red]False[/red]"
    else:
        setting = "[green]"+str(setting)+"[/green]"
    return setting

def do_updates(buckets):
    global s3_client
    for bucket in track(buckets, description="Updating..."):
        s3_client.put_public_access_block(
            Bucket=bucket['Name'],
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )
    return

def main():
    global s3_client
    waiting_for_answer = True

    # Prompt for AWS profile to use
    aws_profile = input("Enter AWS_PROFILE name to use, or leave empty for default: ")
    if not aws_profile:
        aws_session = boto3.Session()
    else:
        aws_session = boto3.Session(profile_name=aws_profile)
    
    s3_client = aws_session.client('s3')

    # Setup table
    table = Table()
    table.add_column("Bucket Name", justify="left", style="cyan", no_wrap=True)
    table.add_column("BlockPublicAcls", justify="left")
    table.add_column("IgnorePublicAcls", justify="left")
    table.add_column("BlockPublicPolicy", justify="left")
    table.add_column("RestrictPublicBuckets", justify="left")

    # Create dict of S3 buckets
    allbuckets = s3_client.list_buckets()['Buckets']

    # Draw table and populate
    with Live(table, refresh_per_second=4):
        for bucket in allbuckets:
            bucket_name = bucket['Name']
            try:
                result = s3_client.get_public_access_block(Bucket=bucket['Name'])
                public_configurations = result['PublicAccessBlockConfiguration']
                block_public_acls = public_configurations.get('BlockPublicAcls')
                ignore_public_acls = public_configurations.get('IgnorePublicAcls')
                block_public_policy = public_configurations.get('BlockPublicPolicy')
                restrict_public_buckets = public_configurations.get('RestrictPublicBuckets')
            except:
                block_public_acls = "Unset"
                ignore_public_acls = "Unset"
                block_public_policy = "Unset"
                restrict_public_buckets = "Unset"
                pass

            # Add the row
            table.add_row(
                f"{bucket_name}",
                f"{set_colour(block_public_acls)}",
                f"{set_colour(ignore_public_acls)}",
                f"{set_colour(block_public_policy)}",
                f"{set_colour(restrict_public_buckets)}"
                )

    print("")
    while(waiting_for_answer):
        answer = input("Apply changes to all buckets? [yes/no] ")
        if answer == "yes": 
            do_updates(allbuckets)
            print("\nComplete")
            exit()
        elif answer == "no": 
            print("Bye")
            exit()
        else: 
            print("Please enter yes or no.")

if __name__== "__main__":
    main()