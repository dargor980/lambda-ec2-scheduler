import boto3

def lambda_handler(event, context):
    ec2 = boto3.resource('ec2')
    
    # Get the action from the event (it can be 'start' or 'stop')
    action = event.get('action')
    
    if not action:
        return {
            'error': "No action specified. Use 'start' or 'stop'."
        }

    # Filter instances with the tag 'AutoStartStop' set to 'True'
    filters = [{
            'Name': 'tag:AutoStartStop',
            'Values': ['True']
        }]
    
    instances = ec2.instances.filter(Filters=filters)

    if action == 'start':
        # Turn on instances that are turned off
        start_instances = [i.id for i in instances if i.state['Name'] == 'stopped']
        if start_instances:
            print("Starting instances:", start_instances)
            ec2.instances.filter(InstanceIds=start_instances).start()
        return {
            'message': f"Started instances: {start_instances}"
        }

    elif action == 'stop':
        # Turn off instances that are running
        stop_instances = [i.id for i in instances if i.state['Name'] == 'running']
        if stop_instances:
            print("Stopping instances:", stop_instances)
            ec2.instances.filter(InstanceIds=stop_instances).stop()
        return {
            'message': f"Stopped instances: {stop_instances}"
        }

    else:
        return {
            'error': "Unrecognized action. Use 'start' or 'stop'."
        }
