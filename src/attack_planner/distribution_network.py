

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
        self.pipes = set() 
  
    def __repr__(self):
        return f"Facility(name={self.name}, max_consumption={self.max_consumption}, max_production={self.max_production})"

    def __str__(self):
        return f"Facility(name={self.name}, max_consumption={self.max_consumption}, max_production={self.max_production})"

class Pipeline:
    def __init__(self, name:str, facilities : list, capacity : float):
        '''
        Args:
            name (str): The name of the pipeline.
            facilities (list): A list of facilities that the pipeline connects.
            capacity (float): The maximum flow capacity of the pipeline.
        '''
        self.name = name
        self.facilities = facilities
        self.capacity = capacity
    
    def __repr__(self):
        return f"Pipeline(name={self.name}, facilities={[facility.name for facility in self.facilities]}, capacity={self.capacity})"
    def __str__(self):
        return f"Pipeline(name={self.name}, facilities={[facility.name for facility in self.facilities]}, capacity={self.capacity})"


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
            facility_names = pipeline_data['facilities']
            facilities = [network.facilities[facility_name] for facility_name in facility_names]
            capacity = pipeline_data['capacity']
            pipeline = Pipeline(name, facilities, capacity)
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
        self.pipelines[pipeline.name] = pipeline