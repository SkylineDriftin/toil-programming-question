

import queue


class Facility:
    '''
    Represents a facility in the distribution network.
    Each facility has a name, maximum consumption, production capacity, 
    and a set of connected pipelines.
    '''

    def __init__(self, name : str, max_consumption : float, max_production : float):
        '''
        Args:
            name (str): The name of the facility.
            max_consumption (float): The maximum consumption capacity of the facility.
            max_production (float): The production capacity of the facility.

        pipes is a set of pipe segments connected to the facility in which the facility is the source, which can be used to determine the flow of resources through the network.
        '''
        self.name = name
        self.max_consumption = max_consumption
        self.max_production = max_production 
        self.pipelines_in = set()
        self.pipelines_out = set()
    

    def add_pipeline(self, pipeline_segment : 'PipelineSegment'):
        if pipeline_segment.source == self:
            self.pipelines_out.add(pipeline_segment)
        elif pipeline_segment.destination == self:
            self.pipelines_in.add(pipeline_segment)
        else:
            raise ValueError(f"Pipeline segment {pipeline_segment} is not connected to facility {self.name}")
    
    def net_production(self):
        '''
        calculates the net production of the facility, which is the production capacity minus the consumption capacity.
        '''
        return self.max_production - self.max_consumption

    def get_total_flow_capacity_to(self, conneccted_facility : 'Facility'):
        total_flow = 0
        for pipeline in self.pipelines_out:
            if pipeline.destination == conneccted_facility:
                total_flow += pipeline.capacity
        return total_flow

    def get_total_flow_capacity_from(self, conneccted_facility : 'Facility'):
        total_flow = 0
        for pipeline in self.pipelines_in:
            if pipeline.source == conneccted_facility:
                total_flow += pipeline.capacity
        return total_flow

    def get_ouput_facilities(self):
        output_facilities = set()
        for pipeline in self.pipelines_out:
            output_facilities.add(pipeline.destination)
        return output_facilities

    def __repr__(self):
        return f"Facility(name={self.name}, max_consumption={self.max_consumption}, max_production={self.max_production}, pipelines: in={self.pipelines_in}, out={self.pipelines_out})"

    def __str__(self):
        return f"Facility(name={self.name}, max_consumption={self.max_consumption}, max_production={self.max_production}, pipelines: in={self.pipelines_in}, out={self.pipelines_out})"
    
class PipelineSegment:
    def __init__(self, name : str, source: Facility, destination : Facility, capacity : float):
        self.name = name
        self.source = source
        self.destination = destination
        self.capacity = capacity
    
    
    def __str__(self):
        return f"PipelineSegment(name={self.name}, source={self.source.name}, destination={self.destination.name}, capacity={self.capacity})"
    def __repr__(self):
        return f"PipelineSegment(name={self.name}, source={self.source.name}, destination={self.destination.name}, capacity={self.capacity})"

        



class DistributionNetwork:
    def __init__(self):
        self.facilities = dict()
    
    @staticmethod
    def from_json(json_data):
        network = DistributionNetwork()
        # iterate through facility data in json, create Facility object, and add to distribution network
        for facility_data in json_data['facilities']:
            name = facility_data['name']
            # check if consumption and/or production data is present, if not set to 0
            max_consumption = facility_data.get('max_consumption', 0)
            max_production = facility_data.get('max_production', 0)
            facility = Facility(name, max_consumption, max_production)
            network.add_facility(facility)
        #iterate through pipeline data in json, create Pipeline object, and add to distribution network
        for pipeline_data in json_data['pipelines']:
            name = pipeline_data['name']
            facility_names = pipeline_data['facilities']
            facilities = [network.facilities[facility_name] for facility_name in facility_names]
            capacity = pipeline_data['capacity']

            for i in range(1, len(facilities)):
                source_facility = facilities[i-1]
                destination_facility = facilities[i]
                pipeline_segment = PipelineSegment(name, source_facility, destination_facility, capacity)
                network.facilities[source_facility.name].add_pipeline(pipeline_segment)
            
        return network
    
    def add_facility(self, facility : Facility):
        '''
        Adds a facility to the distribution network.
        args:
            facility (Facility): The facility to be added to the network.
        '''
        self.facilities[facility.name] = facility
    
    
    def max_consumption(self):
        '''
        calculates the maximum total consumption of the distribution newtwork.

        References: 
            https://en.wikipedia.org/wiki/Maximum_flow_problem
            https://en.wikipedia.org/wiki/Ford%E2%80%93Fulkerson_algorithm
            https://en.wikipedia.org/w/index.php?title=Edmonds%E2%80%93Karp_algorithm&oldid=1319257810
            
            

        the consumption of a facility is limited by its max_consumption, the capacity of the pipelines attached to it, and the amount produced by previous facilities.
        There may also be alternative pipelines by which the resources can flow through the network, so the maximum consumption is not simply the sum of the max_consumption of all facilities.

        it is a known assumption that the pipelines will never loop. This means that the flow of resources through the network can be represented as a directed acyclic graph (DAG), where the facilities are the nodes and the pipelines are the edges.
        This is a max flow problem with multiple sinks and sources in a DAG. 

        This cannot be solved by a simple max-flow solution because of multiple sinks and sources, so we will create a super source and super sink to convert the problem into a single source and single sink max flow problem.
        
        We will then calculate the maximum flow using edmonds-karp algorithm, an implementation of the ford-fulkerson method for computing maximum flow.
        '''


        # connect all producing nodes to super-source with edges of capacity equal to their production
        # connect all consuming nodes to super-sink with edges of capacity equal to their consumption
        
        super_source = Facility('Super Source' , 0, float('inf'))
        super_sink = Facility('Super Sink', float('inf'), 0)        

        
        # make simple pipeline graph for bfs traversal
        pipelines = dict() # pipelines[source_node][dest_node] = remaining capacity from source to destination (start at total capacity)
        pipelines[super_source] =  dict()
        pipelines[super_sink] = dict()

        for facility in self.facilities.values():
            if facility not in pipelines:
                pipelines[facility] = dict()
            if facility.max_production > 0:
                pipelines[super_source][facility] = facility.max_production
            if facility.max_consumption > 0:
                pipelines[facility][super_sink] = facility.max_consumption
            for pipeline in facility.pipelines_out:
                source_node = pipeline.source
                dest_node = pipeline.destination
                if dest_node not in pipelines[source_node]:
                    pipelines[source_node][dest_node] = 0
                pipelines[source_node][dest_node] += pipeline.capacity
            print(f"facilty: {facility.name}, connected nodes:")
            for dest_node, capacity in pipelines.get(facility, dict()).items(): 
                print(f"\t{dest_node.name} with capacity {capacity}")
        print("facility: super source, connected nodes:")
        for dest_node, capacity in pipelines.get(super_source, dict()).items():
            print(f"\t{dest_node.name} with capacity {capacity}")
        
        # using psuedocode from the edmonds-karp wikipedia page, we will implement the algorithm to calculate the maximum flow from super-source to super-sink in the network.
        # note that beccause the super-sink represents the total consumption, 
        total_consumption = 0 

        # edge_flows[source_node][dest_node] = current flow from source to destination
        flow = 0   #Initialize flow to zero
        iteration  = 0 
        while True:
            # bfs from source to sink to find an augmenting path
            q = queue.Queue()
            q.put(super_source)
            prev_of = {super_source : None } # store previous node traversed of each node here
            while not q.empty():
                current_node = q.get()
                # chheck forwards nodes
                for dest_node, capacity in pipelines.get(current_node, dict()).items(): # iterate through the conected node and the pipeline capacity of each connected note
                    print(iteration)
                    iteration += 1
                    if dest_node not in prev_of and capacity > 0: # if the node has not been traversed and there is remaining capacity in the pipeline
                        prev_of[dest_node] = current_node
                        q.put(dest_node)
                print('iterated one')
            print('escaped loop')
            if super_sink in prev_of:
                print('found path')
                #found path, time to calculate the flow through the path and update the capacities of the pipelines accordingly
                path_flow = float('inf')
                current_node = super_sink 
                while prev_of[current_node] is not None:
                    prev_node = prev_of[current_node]
                    path_flow = min(path_flow, pipelines[prev_node][current_node]) # flow  limited by smallest pipe capacity
                    current_node = prev_of[current_node]
                print('frozen here')
                # update capacities of pipelines along the path
                current_node = super_sink
                while prev_of[current_node] is not None:
                    prev_node = prev_of[current_node]
                    pipelines[prev_node][current_node] -= path_flow
                    
                    # initiate reverse edge if does not exist
                    if current_node not in pipelines: 
                        pipelines[current_node] = {} 
                    if prev_node not in pipelines[current_node]: 
                        pipelines[current_node][prev_node] = 0
                    pipelines[current_node][prev_node] += path_flow

                    current_node = prev_node
                print('failed here')
                
                total_consumption += path_flow
            else:
                #no path found, we have reached the maximum flow
                break
        return total_consumption
    




                             

        
        

    
    def __repr__(self):
        return f"DistributionNetwork(facilities={self.facilities}, pipelines={self.pipelines})"
    def __str__(self):
        return f"DistributionNetwork(facilities={self.facilities}, pipelines={self.pipelines})"
    
    
