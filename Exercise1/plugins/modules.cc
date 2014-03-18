#include "FWCore/Framework/interface/ModuleFactory.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "RecoBTau/JetTagComputer/interface/JetTagComputerESProducer.h"
#include "BTagTutorial/Exercise1/interface/ShrinkConeTrackCountingComputer.h"
#include "BTagTutorial/Exercise1/interface/SumTrackCountingComputer.h"

typedef JetTagComputerESProducer<ShrinkConeTrackCountingComputer> ShrinkConeTrackCountingESProducer;
DEFINE_FWK_EVENTSETUP_MODULE(ShrinkConeTrackCountingESProducer);

typedef JetTagComputerESProducer<SumTrackCountingComputer> SumTrackCountingESProducer;
DEFINE_FWK_EVENTSETUP_MODULE(SumTrackCountingESProducer);

