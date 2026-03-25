

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

        pipelines is a set of facilities that are connected to this facility via pipelines.
        '''
        self.name = name
        self.max_consumption = max_consumption
        self.max_production = max_production 
        self.pipelines = set() 
  
    def __repr__(self):
        return f"Facility(name={self.name}, max_consumption={self.max_consumption}, max_production={self.max_production})"

    def __str__(self):
        return f"Facility(name={self.name}, max_consumption={self.max_consumption}, max_production={self.max_production})"

class Pipeline:
    '''
    Represents a directional pipeline connecting two facilities in the distribution network.
    '''
    def __init__(self, name : str, source : Facility, destination : Facility):
        '''
        Args:
            source (Facility): The source facility of the pipeline.
            destination (Facility): The destination facility of the pipeline.
        '''
        self.name = name 
        self.source = source
        self.destination = destination



class DistributionNetwork:
    def __init__(self):
        self.facilities = dict()
        self.pipelines = dict()
    
    @staticmethod
    def from_json(json_data):
        network = DistributionNetwork()
        # iterate through facility data in json, create Facility object, and add to distribution network
        for facility_data in json_data['facilities']:
            name = facility_data['name']
            # check if consumption and/or production data is present, if not set to 0
            if max_consumption := facility_data.get('max_consumption') is not None:
                max_consumption = facility_data['max_consumption']
            else:
                max_consumption = float(0)
            if max_production := facility_data.get('max_production') is not None:
                max_production = facility_data['max_production']
            else:
                max_production = float(0)
            facility = Facility(name, max_consumption, max_production)
            network.add_facility(facility)
        #iterate through pipeline data in json, create Pipeline object, and add to distribution network
        for pipeline_data in json_data['pipelines']:
            name = pipeline_data['name']
            source_name = pipeline_data['source']
            destination_name = pipeline_data['destination']
            source = network.facilities[source_name]
            destination = network.facilities[destination_name]
            pipeline = Pipeline(name, source, destination)
            network.add_pipeline(pipeline)
        
        
        return network
    
    def add_facility(self, facility : Facility):
        '''
        Adds a facility to the distribution network.
        args:
            facility (Facility): The facility to be added to the network.
        '''
        self.facilities[facility.name] = facility
    
    
    def add_pipeline(self, pipeline : Pipeline):
        '''
        Adds a pipeline to the distribution network and updates the connected facilities.
        args:
            pipeline (Pipeline): The pipeline to be added to the network.
        '''
        self.pipelines[pipeline.name] = pipeline
        pipeline.source.pipelines.add(pipeline)
        pipeline.destination.pipelines.add(pipeline)
    
    def __repr__(self):
        return f"DistributionNetwork(facilities={list(self.facilities.keys())})"
    def __str__(self):
        return f"DistributionNetwork(facilities={list(self.facilities.keys())})"