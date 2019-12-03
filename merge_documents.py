'''
   Given a set of document schema, merged document schema
   and document samples, write a function suite to merge
   the set of documents based on a set of rules.
'''

import datetime

#######################################
# document schema
#######################################

@dataclass(frozen=True, order=True)
class Properties:
    domain:             str
    timestamp:          datetime.datetime
    source:             str
    source_trust_score: int


@dataclass(frozen=True, order=True)
class Content:
    text:           FrozenSet[str] = field(default_factory=frozenset)


@dataclass(frozen=True, order=True)
class Coordinates:
    lat:            float
    lon:            float


@dataclass(frozen=True, order=True)
class Location:
    country:        Optional[str] = None
    city:           Optional[str] = None
    district:       Optional[str] = None
    coordinates:    Optional[Coordinates] = None


@dataclass(frozen=True, order=True)
class Geo:
    location:       Optional[Location] = None


@dataclass(frozen=True, order=True)
class Round:
    type:           Optional[str] = None
    amount:         Optional[int] = None


@dataclass(frozen=True, order=True)
class Funding:
    rounds:         FrozenSet[Round] = field(default_factory=frozenset)


@dataclass(frozen=True, order=True)
class Data:
    content:        Optional[Content] = None
    geo:            Optional[Geo] = None
    funding:        Optional[Funding] = None


@dataclass(frozen=True, order=True)
class Document:
    properties:     Properties
    data:           Data


#######################################
# merged document schema
#######################################

@dataclass(frozen=True, order=True)
class MergedContent:
    # rule: take values from all sources
    text:           FrozenSet[str] = field(default_factory=frozenset)


@dataclass(frozen=True, order=True)
class MergedGeo:
    # rule: values from all sources
    location_all:   FrozenSet[Location] = field(default_factory=frozenset)
    # rule: value has to be chosen based on a combination of data age and source_trust_score
    location:       Optional[Location] = None


@dataclass(frozen=True, order=True)
class MergedFunding:
    # rule: values from all sources
    rounds_all:     FrozenSet[Round] = field(default_factory=frozenset)
    # rule: value has to be chosen based on a combination of data age and source source_trust_score
    rounds:         FrozenSet[Round] = field(default_factory=frozenset)


@dataclass(frozen=True, order=True)
class MergedData:
    content:        Optional[MergedContent] = None
    geo:            Optional[MergedGeo] = None
    funding:        Optional[MergedFunding] = None


@dataclass(frozen=True, order=True)
class MergedDocument:
    properties:     FrozenSet[Properties]
    data:           MergedData


##############################
# Document Samples
##############################

documents = [
    Document(
        properties=Properties(
            domain="startus.cc",
            source="source1",
            timestamp=datetime.datetime(2017, 5, 12),
            source_trust_score=2
        ),
        data=Data(
            content=Content(text=frozenset(["Lorem ipsum"])),
            geo=Geo(
                location=Location(
                    country="Austria",
                    city="Vienna",
                    district="Mariahilf",
                    coordinates=Coordinates(lat=48.1964, lon=16.3516)
                )
            )
        ),
    ),
    Document(
        properties=Properties(
            domain="startus.cc",
            source="source1",
            timestamp=datetime.datetime(2017, 5, 13),
            source_trust_score=2
        ),
        data=Data(
            content=Content(text=frozenset(["dolor sir amlet"]))
        )
    ),
    Document(
        properties=Properties(
            domain="startus.cc",
            source="source2",
            timestamp=datetime.datetime(2018, 7, 3),
            source_trust_score=6
        ),
        data=Data(
            geo=Geo(
                location=Location(
                    country="Austria",
                    city="Vienna",
                    coordinates=Coordinates(lat=48.2082, lon=16.3738)
                )
            ),
            funding=Funding(
                rounds=frozenset(
                    [
                        Round(type="Some round 1", amount=100000),
                        Round(type="Some round 2", amount=100000)
                    ]
                )
            )
        )
    ),
    Document(
        properties=Properties(
            domain="startus.cc",
            source="source3",
            timestamp=datetime.datetime(2019, 9, 12),
            source_trust_score=5
        ),
        data=Data(
            geo=Geo(
                location=Location(
                    country="Albania",
                    coordinates=Coordinates(lat=41.1533, lon=20.1683)
                )
            ),
            funding=Funding(
                rounds=frozenset(
                    [
                        Round(type="Some round 1", amount=100000),
                        Round(type="Some round 5", amount=100000)
                    ]
                )
            )
        )
    )
]

####################################
# Functions to merge documents
####################################

def apply_rule(doc_data_age, doc_trust_age, data_age_used):    
    if doc_data_age <= data_age_used: 
        if doc_trust_age >= 4:
            return True
        else:
            return False
    else:
        return False


def get_current_properties(doc):
    curr_properties = Properties(domain=doc.properties.domain, 
                                 timestamp=doc.properties.timestamp, 
                                 source=doc.properties.source, 
                                 source_trust_score=doc.properties.source_trust_score)
    
    return curr_properties


def get_current_content(doc):
    if doc.data.content:
        cont, *_ = doc.data.content.text
        return cont
    else:
        return None


def get_current_location(doc):
    curr_location = None 
    if doc.data.geo:
        if doc.data.geo.location:
            if doc.data.geo.location.country:
                curr_country = doc.data.geo.location.country
            else:
                curr_country = None
            
            if doc.data.geo.location.city:
                curr_city = doc.data.geo.location.city
            else:
                curr_city = None
                
            if doc.data.geo.location.district:
                curr_district = doc.data.geo.location.district
            else:
                curr_district = None
            
            if doc.data.geo.location.coordinates:
                curr_coordinates = Coordinates(lat=doc.data.geo.location.coordinates.lat, 
                                          lon=doc.data.geo.location.coordinates.lon)
            else:
                curr_coordinates = None
    
            curr_location = Location(country=curr_country, 
                                     city=curr_city, 
                                     district=curr_district, 
                                     coordinates=curr_coordinates)
    
    return curr_location


def get_current_rounds(doc):
    curr_rounds = None
    if doc.data.funding:
        return doc.data.funding.rounds
    else:
        return None


def create_merged_document_obj(merged_properties, merged_content, merged_locations, location_to_use, merged_rounds, rounds_to_use):
    merged_properties = frozenset(merged_properties)
    merged_data = MergedData(content=MergedContent(text=frozenset(merged_content)),
                             geo=MergedGeo(location_all=frozenset(merged_locations), location=location_to_use), 
                             funding=MergedFunding(rounds_all=frozenset(merged_rounds), 
                                                   rounds=frozenset(rounds_to_use)))

    merged_document = MergedDocument(properties=merged_properties, data=merged_data)
    
    return merged_document


def merge_documents():
    merged_properties = []
    merged_content = []
    merged_locations  = []
    merged_rounds = []
    location_to_use = Location()
    rounds_to_use = []
    data_age_used = 0
    trust_score_used = 0

    today_date = datetime.datetime.now()

    for index in range(0, len(documents)):
        curr_doc = documents[index]
        if index == 0:
            data_age_used = (today_date - curr_doc.properties.timestamp).days
        else:
            doc_data_age = (today_date - curr_doc.properties.timestamp).days
            doc_trust_score = curr_doc.properties.source_trust_score
    
        curr_properties = get_current_properties(curr_doc)
        merged_properties.append(curr_properties)
    
        curr_content = get_current_content(curr_doc)
        if curr_content is not None:
            merged_content.append(curr_content)
        
        curr_location = get_current_location(curr_doc)
        if curr_location is not None:
            merged_locations.append(curr_location)
        
        if index == 0:
            location_to_use = curr_location
        else:
            if apply_rule(doc_data_age, doc_trust_score, data_age_used):
                location_to_use = curr_location
         
        
        curr_rounds_in_doc = []
        curr_rounds = get_current_rounds(curr_doc)
        if curr_rounds is not None:
            for curr_round in curr_rounds:
                merged_rounds.append(curr_round)
                curr_rounds_in_doc.append(curr_round)
        
        if index == 0:
            rounds_to_use = curr_rounds_in_doc
        else:
            if apply_rule(doc_data_age, doc_trust_score, data_age_used) and curr_rounds != []:
                rounds_to_use = curr_rounds_in_doc
             
    merged_document = create_merged_document_obj(merged_properties, merged_content, merged_locations, location_to_use, merged_rounds, rounds_to_use)

    return merged_document

if __name__ == "__main__":
    merged = merge_documents()
    print(merged)






