#include "FWCore/Framework/interface/ModuleFactory.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "BTagTutorial/Exercise1/interface/ShrinkConeTrackCountingComputer.h"

typedef JetTagComputerESProducer<ShrinkConeTrackCountingComputer> ShrinkConeTrackCountingESProducer;
DEFINE_FWK_EVENTSETUP_MODULE(ShrinkConeTrackCountingESProducer);

