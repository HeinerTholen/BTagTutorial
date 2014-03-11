#ifndef ImpactParameter_ShrinkConeTrackCountingComputer_h
#define ImpactParameter_ShrinkConeTrackCountingComputer_h

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/BTauReco/interface/TrackCountingTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"
#include "Math/GenVector/VectorUtil.h"
#include "RecoBTau/JetTagComputer/interface/JetTagComputer.h"

#include "TF1.h"

class ShrinkConeTrackCountingComputer : public JetTagComputer
{
 public:
  ShrinkConeTrackCountingComputer(const edm::ParameterSet  & parameters )
  {
     m_nthTrack         = parameters.getParameter<int>("nthTrack");
     m_ipType           = parameters.getParameter<int>("impactParameterType");
     m_deltaR           = parameters.getParameter<double>("deltaR");
     m_cutMaxDecayLen   = parameters.getParameter<double>("maximumDecayLength"); //used
     m_cutMaxDistToAxis = parameters.getParameter<double>("maximumDistanceToJetAxis"); //used
     //
     // access track quality class; "any" takes everything
     //
     std::string trackQualityType = parameters.getParameter<std::string>("trackQualityClass"); //used
     m_trackQuality =  reco::TrackBase::qualityByName(trackQualityType);
     m_useAllQualities = false;
     if (trackQualityType == "any" || 
	 trackQualityType == "Any" || 
	 trackQualityType == "ANY" ) m_useAllQualities = true;

     uses("ipTagInfos");

     // my cone function (x<100.: 0.5, x>1000: 0.1, else: linear scaling)
     m_coneFunc = TF1("my_cone_func", "(x<100.)? 0.51 : ((x>1000.)? 0.1 : (100.-x)*4./9000.+0.5)", 0., 1000.);
  }
  
 
  float discriminator(const TagInfoHelper & ti) const 
   {
    const reco::TrackIPTagInfo & tkip = ti.get<reco::TrackIPTagInfo>();
    std::multiset<float> significances = orderedSignificances(tkip);
    std::multiset<float>::reverse_iterator nth=significances.rbegin();
    for(int i=0;i<m_nthTrack-1 && nth!=significances.rend();i++) nth++;  
     if(nth!=significances.rend()) return *nth; else return -100.;
   }

 protected:
     std::multiset<float> orderedSignificances(const reco::TrackIPTagInfo & tkip)   const  {

          const std::vector<reco::TrackIPTagInfo::TrackIPData> & impactParameters((tkip.impactParameterData()));
          const edm::RefVector<reco::TrackCollection> & tracks(tkip.selectedTracks());
          std::multiset<float> significances;
          int i=0;
          if(tkip.primaryVertex().isNull())  {  return std::multiset<float>();}

          GlobalPoint pv(tkip.primaryVertex()->position().x(),tkip.primaryVertex()->position().y(),tkip.primaryVertex()->position().z());

          for(std::vector<reco::TrackIPTagInfo::TrackIPData>::const_iterator it = impactParameters.begin(); it!=impactParameters.end(); ++it, i++)
           {
           if(   fabs(impactParameters[i].distanceToJetAxis.value()) < m_cutMaxDistToAxis  &&        // distance to JetAxis
                 (impactParameters[i].closestToJetAxis - pv).mag() < m_cutMaxDecayLen  &&      // max decay len
		 (m_useAllQualities  == true || (*tracks[i]).quality(m_trackQuality)) // use selected track qualities
             )
	     {
                if(ROOT::Math::VectorUtil::DeltaR((*tkip.jet()).p4().Vect(), (*tracks[i]).momentum()) < m_coneFunc.Eval((*tkip.jet()).pt()))
                 significances.insert( ((m_ipType==0)?it->ip3d:it->ip2d).significance() );
              }
          }
 
         return significances;    
   }


    
   int m_nthTrack;
   int m_ipType;
   double m_deltaR;
   double  m_cutMaxDecayLen;
   double m_cutMaxDistToAxis;
   reco::TrackBase::TrackQuality   m_trackQuality;
   bool m_useAllQualities;

   // my cone function
   TF1 m_coneFunc;
};

#endif // ImpactParameter_ShrinkConeTrackCountingComputer_h
