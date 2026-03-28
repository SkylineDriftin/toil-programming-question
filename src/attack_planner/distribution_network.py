import igraph 


class DistributionNetwork:
    def __init__(self):
        self.graph = igraph.Graph(directed=True)
        
        self.facilities = dict() # facility_name : facility_index
        self.pipelines = [] #save edge pipeline data for later reference
        
        #super source and sink nodes
        self.graph.add_vertices(2) # add super source and sink nodes
        self.source_index = 0
        self.sink_index = 1
    
        
    def add_facility(self, facility_name, max_production=0, max_consumption=0):
        # add facility to graph and connect to super source/sink as appropriate
        new_facility = self.graph.add_vertex(name=facility_name)
        self.facilities[facility_name] = new_facility.index
        
        if max_production > 0 :
            self.graph.add_edge(self.source_index, new_facility.index, capacity=float(max_production))
        if max_consumption > 0:
            self.graph.add_edge(new_facility.index, self.sink_index, capacity=float(max_consumption))
        
        return new_facility.index
    
    def add_pipeline(self, pipeline_name, facility_names, capacity):
        capacity = float(capacity)

        for i in range(1, len(facility_names)):
            f1_name = facility_names[i-1]
            f2_name = facility_names[i]

            if f1_name == f2_name:
                continue

            f_idx_1 = self.facilities[f1_name]
            f_idx_2 = self.facilities[f2_name]

            # make sure edges are bidirectional
            pipeline_metadata  = {
                'pipeline_name' : pipeline_name,
                'between' : sorted([f1_name, f2_name]),
                'max_capacity' : capacity
            }
            
            e12 = self.graph.add_edge(f_idx_1, f_idx_2, capacity=capacity, payload=pipeline_metadata)
            e21 = self.graph.add_edge(f_idx_2, f_idx_1, capacity=capacity, payload=pipeline_metadata)
            pipeline_metadata['edge_indices'] = (e12.index, e21.index)
            self.pipelines.append(pipeline_metadata)
        
    @classmethod
    def from_json(cls, json_data):
        #first, we set up a rustworkx digraph to represent the nodes
        # facilities
        network  = cls()

        for facility in json_data['facilities']:
            facility_name = facility['name']
            max_production = facility.get('max_production', 0)
            max_consumption = facility.get('max_consumption', 0)
            network.add_facility(facility_name, max_production, max_consumption)
            
        # pipelines
        for pipe in json_data['pipelines']:
            name = pipe['name']
            facility_names = pipe['facilities']
            capacity = float(pipe['capacity'])

            network.add_pipeline(name, facility_names, capacity)
        
        return network
    
    def calculate_max_consumption(self):
        # note max consumption will be equal to max flow from super source to super sink
        
        if self.graph.ecount() == 0:
            return 0.0
        # theres no need to calculate max flow if there are no edges in the graph
        
        flow = self.graph.maxflow(self.source_index, self.sink_index, capacity='capacity')
        return flow.value
    
    def plan_attack(self):
        # find mincut edges and simulate across only those edges
        initial_flow = self.graph.maxflow(self.source_index, self.sink_index, capacity='capacity')
        

        if initial_flow.value == 0:
            return {
                "pipeline_name": None,
                "between": [],
                "total_consumption_before": 0.0,
                "total_consumption_after": 0.0
            }

        mincut_edge_indices = initial_flow.cut

        best_flow = initial_flow.value
        best_segment = None

        viewed_segments = set() # prevent duplicate checks for fwd and rev edges on digrah

        candidate_metadata = []
        for edge_idx in mincut_edge_indices:
            edge = self.graph.es[edge_idx]
            # only look at edges that have our pipeline metadata
            if 'payload' in edge.attributes() and edge['payload'] is not None:
                pipeline_metadata = edge['payload']
                e_12_idx, e_21_idx = pipeline_metadata['edge_indices']
                segment_key = tuple(sorted((e_12_idx, e_21_idx)))
                
                if segment_key not in viewed_segments:
                    candidate_metadata.append(pipeline_metadata)
                    viewed_segments.add(segment_key)

        if not candidate_metadata:
            search_set = self.pipelines
        else:
            search_set = candidate_metadata
        

        for segment in search_set:
            e_12_idx, e_21_idx = segment['edge_indices']

            # set edge capacities to zero temporarily
            cap = self.graph.es[e_12_idx]['capacity']
            try:
                self.graph.es[e_12_idx]['capacity'] = 0
                self.graph.es[e_21_idx]['capacity'] = 0

                # calculate new flow
                new_flow = self.graph.maxflow(self.source_index, self.sink_index, capacity='capacity').value
                
                #update flow if this reduces flow
                if new_flow < best_flow:
                    best_flow = new_flow
                    best_segment = segment
            finally:
                # reset edge capacities
                self.graph.es[e_12_idx]['capacity'] = cap
                self.graph.es[e_21_idx]['capacity'] = cap
            
        if not best_segment:
            return {
                'pipeline_name': None,
                'between': [],
                'total_consumption_before': initial_flow.value,
                'total_consumption_after': initial_flow.value
            }

        result = {
            'pipeline_name' : best_segment['pipeline_name'],
            'between' : best_segment['between'],
            'total_consumption_before' : initial_flow.value,
            'total_consumption_after' : best_flow
        }
        return result
