
import FWCore.ParameterSet.Config as cms

process = cms.Process("validation")

# load the full reconstraction configuration, to make sure we're getting all needed dependencies
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

# for the conditions
from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = autoCond['startup']


######################################################### Ex: Initial Setup ###
process.MyAk5PFJetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
    process.j2tParametersVX,
    jets = cms.InputTag("ak5PFJets")
)

process.MyImpactParameterPFTagInfos = process.impactParameterTagInfos.clone(
    jetTracks = "MyAk5PFJetTracksAssociatorAtVertex"
)

process.MyTrackCountingHighEffBJetTags = process.trackCountingHighEffBJetTags.clone(
    tagInfos = cms.VInputTag(cms.InputTag("MyImpactParameterPFTagInfos"))
)

process.load("BTagTutorial.Exercise1.shrinkConeTrackCountingHighEffBJetTags_cfi")
process.MyShrinkConeTrackCountingHighEffBJetTags = process.shrinkConeTrackCountingHighEffBJetTags.clone(
    tagInfos = cms.VInputTag(cms.InputTag("MyImpactParameterPFTagInfos"))
)

process.load("BTagTutorial.Exercise1.trackCountingSuperHighEffBJetTags_cfi")
process.MyTrackCountingSuperHighEffBJetTags = process.trackCountingSuperHighEffBJetTags.clone(
    tagInfos = cms.VInputTag(cms.InputTag("MyImpactParameterPFTagInfos"))
)

process.MyTrackCountingHighPurBJetTags = process.trackCountingHighPurBJetTags.clone(
    tagInfos = cms.VInputTag(cms.InputTag("MyImpactParameterPFTagInfos"))
)

process.load("BTagTutorial.Exercise1.trackCountingSuperHighPurBJetTags_cfi")
process.MyTrackCountingSuperHighPurBJetTags = process.trackCountingSuperHighPurBJetTags.clone(
    tagInfos = cms.VInputTag(cms.InputTag("MyImpactParameterPFTagInfos"))
)

process.MySecondaryVertexTagInfos = process.secondaryVertexTagInfos.clone(
    trackIPTagInfos = cms.InputTag("MyImpactParameterPFTagInfos")
)

process.MySimpleSecondaryVertexHighEffBJetTags = process.simpleSecondaryVertexHighEffBJetTags.clone(
    tagInfos = cms.VInputTag(cms.InputTag("MySecondaryVertexTagInfos"))
)

##################################################### Ex: Performance Plots ###
process.load("PhysicsTools.JetMCAlgos.CaloJetsMCFlavour_cfi")

process.AK5PFbyRef = process.AK5byRef.clone(
  jets = "ak5PFJets"
)

process.AK5PFbyValAlgo = process.AK5byValAlgo.clone(
  srcByReference = "AK5PFbyRef"
)

process.load("DQMServices.Components.DQMEnvironment_cfi")
process.load("DQMServices.Core.DQM_cfg")
process.load("Validation.RecoB.bTagAnalysis_cfi")
process.MybTagValidation = process.bTagValidation.clone(
  jetMCSrc = 'AK5PFbyValAlgo',
  tagConfig = cms.VPSet(
  cms.PSet(
            process.bTagTrackIPAnalysisBlock,
            type = cms.string('TrackIP'),
            label = cms.InputTag("MyImpactParameterPFTagInfos"),
            folder = cms.string("IPTag")
        ),
  cms.PSet(
            process.bTagTrackCountingAnalysisBlock,
            label = cms.InputTag("MyTrackCountingHighEffBJetTags"),
            folder = cms.string("TCHE")
        ),
  cms.PSet(
            process.bTagTrackCountingAnalysisBlock,
            label = cms.InputTag("MyShrinkConeTrackCountingHighEffBJetTags"),
            folder = cms.string("SCTCHE")
        ),
  cms.PSet(
            process.bTagTrackCountingAnalysisBlock,
            label = cms.InputTag("MyTrackCountingSuperHighEffBJetTags"),
            folder = cms.string("TCSHE")
        ),
  cms.PSet(
            process.bTagTrackCountingAnalysisBlock,
            label = cms.InputTag("MyTrackCountingHighPurBJetTags"),
            folder = cms.string("TCHP")
        ),
  cms.PSet(
            process.bTagTrackCountingAnalysisBlock,
            label = cms.InputTag("MyTrackCountingSuperHighPurBJetTags"),
            folder = cms.string("TCSHP")
        ),
  cms.PSet(
            process.bTagSimpleSVAnalysisBlock,
            label = cms.InputTag("MySimpleSecondaryVertexHighEffBJetTags"),
            folder = cms.string("SimpleSVHE")
        )
  )
)

process.dqmEnv.subSystemFolder = 'BTAG'
process.dqmSaver.producer = 'DQM'
process.dqmSaver.workflow = '/POG/BTAG/BJET'
process.dqmSaver.convention = 'Offline'
process.dqmSaver.saveByRun = cms.untracked.int32(-1)
process.dqmSaver.saveAtJobEnd = cms.untracked.bool(True)
process.dqmSaver.forceRunNumber = cms.untracked.int32(1)


process.plots = cms.Path(
    process.MyAk5PFJetTracksAssociatorAtVertex *
    process.MyImpactParameterPFTagInfos *
    process.MySecondaryVertexTagInfos *
    process.MyTrackCountingHighEffBJetTags *
    process.MyShrinkConeTrackCountingHighEffBJetTags *
    process.MyTrackCountingSuperHighEffBJetTags *
    process.MyTrackCountingHighPurBJetTags *
    process.MyTrackCountingSuperHighPurBJetTags *
    process.MySimpleSecondaryVertexHighEffBJetTags *
    process.myPartons *
    process.AK5PFbyRef *
    process.AK5PFbyValAlgo *
    process.MybTagValidation *
    process.dqmSaver
)

process.out = cms.OutputModule("PoolOutputModule",
    outputCommands = cms.untracked.vstring('keep *'),
    fileName = cms.untracked.string('/afs/desy.de/user/t/tholenhe/xxl-af-cms/samples/bTagTutOut.root')
)

process.output = cms.EndPath(
    process.out
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
      "file:/afs/desy.de/user/t/tholenhe/xxl-af-cms/samples/syncExercise53.root"
    )
)
