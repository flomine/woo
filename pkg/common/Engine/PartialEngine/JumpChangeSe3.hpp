// 2008 © Václav Šmilauer <eudoxos@arcig.cz> 
#pragma once

#include<yade/core/PartialEngine.hpp>
#include<yade/core/PhysicalParameters.hpp>
#include<yade/pkg-common/RigidBodyParameters.hpp>

/* Engine that applies sudden change of se3 on subscribed bodies if active.
 *
 * the amount deltaSe3 will be "added" to the current se3 (positions vector-added,
 * orientations composed by quaternion multiplication).
 *
 * if setVelocities is true, velocity and angularVelocity are modified in such a way that over one iteration (dt),
 * the body will have prescribed se3 jump. In this case, se3 itself is not updated for dynamic bodies, since they would
 * have the delta applied twice (here and in the integrator). For non-dynamic bodies however, se3 _is_ updated.
 *
 */
class JumpChangeSe3: public PartialEngine {
	public:
		JumpChangeSe3(){deltaSe3.position=Vector3r::ZERO; deltaSe3.orientation=Quaternionr::IDENTITY; setVelocities=false;};
		virtual ~JumpChangeSe3(){};
		virtual void applyCondition(Scene* mb){
			FOREACH(body_id_t id, subscribedBodies){
				const shared_ptr<Body>& b=Body::byId(id,mb);
				if(setVelocities){
					Real dt=Omega::instance().getTimeStep();
					body->state->vel=deltaSe3.position/dt;
					Vector3r axis; Real angle; deltaSe3.orientation.ToAxisAngle(axis,angle); axis.Normalize();
					body->state->angVel=axis*angle/dt;
					LOG_DEBUG("Angular velocity set to "<<axis*angle/dt<<". Axis="<<axis<<", angle="<<angle);
				}
				if(!setVelocities || (setVelocities && !b->isDynamic)){
					b->state->pos+=deltaSe3.position;
					b->state->ori=deltaSe3.orientation*se3.orientation;
				}
			}
		}
		Se3r deltaSe3;
		bool setVelocities; /* should be bool, but serializer breaks on that */
	REGISTER_ATTRIBUTES(PartialEngine,(deltaSe3)(setVelocities));
	REGISTER_CLASS_NAME(JumpChangeSe3);
	REGISTER_BASE_CLASS_NAME(PartialEngine);
	DECLARE_LOGGER;
};
REGISTER_SERIALIZABLE(JumpChangeSe3);
	
