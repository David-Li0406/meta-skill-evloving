import Navbar from '@/components/Navbar';
import Hero from '@/components/Hero';
import ModuleCard from '@/components/ModuleCard';
import Footer from '@/components/Footer';
import { modules } from '@/data/modules';
import { paths } from '@/data/paths';
import LearningPathCard from '@/components/LearningPathCard';

export default function Home() {
  return (
    <>
      <Navbar />

      {/* Hero Section */}
      <Hero />

      {/* Learning Paths (content-oriented progression) */}
      <section id="paths" className="section-padding bg-slate-900/20">
        <div className="container-custom">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Learning Paths</h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">Curated sequences to master microservices efficiently.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {paths.map((p) => (
              <LearningPathCard key={p.id} path={p} />
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="section-padding">
        <div className="container-custom">
            <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Why Learn <span className="text-brand">Microservices</span>?
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              Master the architecture that powers Netflix, Amazon, Uber, and other tech giants.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Feature 1 */}
            <div className="card group">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-purple-500/20 to-purple-500/5 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-7 h-7 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Scalable Architecture</h3>
              <p className="text-slate-400">Build systems that scale horizontally. Handle millions of users with distributed services.</p>
            </div>

            {/* Feature 2 */}
            <div className="card group">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500/20 to-blue-500/5 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-7 h-7 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Fast Deployments</h3>
              <p className="text-slate-400">Deploy individual services independently. Ship features faster without risking the entire system.</p>
            </div>

            {/* Feature 3 */}
            <div className="card group">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-cyan-500/5 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-7 h-7 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Fault Tolerant</h3>
              <p className="text-slate-400">One service failure doesn't bring down the entire application. Build resilient systems.</p>
            </div>

            {/* Feature 4 */}
            <div className="card group">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-pink-500/20 to-pink-500/5 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-7 h-7 text-pink-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Team Autonomy</h3>
              <p className="text-slate-400">Small teams own individual services. Work independently with different technologies.</p>
            </div>

            {/* Feature 5 */}
            <div className="card group">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-orange-500/20 to-orange-500/5 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-7 h-7 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Technology Freedom</h3>
              <p className="text-slate-400">Use the best technology for each service. No more one-size-fits-all constraints.</p>
            </div>

            {/* Feature 6 */}
            <div className="card group">
              <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-green-500/20 to-green-500/5 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                <svg className="w-7 h-7 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">In-Demand Skills</h3>
              <p className="text-slate-400">Microservices expertise is highly valued. Boost your career with architecture skills.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Modules Section */}
      <section id="modules" className="section-padding bg-slate-900/30">
        <div className="container-custom">
          <div className="text-center mb-16">
            <span className="badge badge-intermediate mb-4">15 Comprehensive Modules</span>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Complete <span className="text-brand">Curriculum</span>
            </h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              From beginner fundamentals to advanced production deployment. Everything you need to master microservices.
            </p>
          </div>

          {/* Beginner Modules */}
          <div className="mb-12">
            <h3 className="text-sm font-semibold text-green-400 uppercase tracking-wider mb-6 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-green-400"></span>
              Fundamentals
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {modules.filter(m => m.difficulty === 'beginner').map((module) => (
                <ModuleCard key={module.slug} {...module} />
              ))}
            </div>
          </div>

          {/* Intermediate Modules */}
          <div className="mb-12">
            <h3 className="text-sm font-semibold text-yellow-400 uppercase tracking-wider mb-6 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-yellow-400"></span>
              Intermediate
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {modules.filter(m => m.difficulty === 'intermediate').map((module) => (
                <ModuleCard key={module.slug} {...module} />
              ))}
            </div>
          </div>

          {/* Advanced Modules */}
          <div>
            <h3 className="text-sm font-semibold text-red-400 uppercase tracking-wider mb-6 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-red-400"></span>
              Advanced
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {modules.filter(m => m.difficulty === 'advanced').map((module) => (
                <ModuleCard key={module.slug} {...module} />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="section-padding">
        <div className="container-custom">
            <div className="text-center mb-12">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Technologies You'll <span className="text-brand">Master</span>
              </h2>
          </div>

          <div className="flex flex-wrap justify-center gap-6">
            {['NestJS', 'Node.js', 'Docker', 'Kubernetes', 'RabbitMQ', 'Kafka', 'PostgreSQL', 'MongoDB', 'Redis', 'Prometheus', 'Grafana', 'GitHub Actions'].map((tech) => (
              <div key={tech} className="px-6 py-3 glass rounded-xl text-slate-300 hover:text-white hover:border-purple-500/50 transition-all duration-300 cursor-default">
                {tech}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section-padding">
        <div className="container-custom">
          <div className="relative rounded-3xl overflow-hidden">
            {/* Background */}
            <div className="absolute inset-0 bg-gradient-to-br from-purple-600/20 via-blue-600/20 to-cyan-600/20"></div>
            <div className="absolute inset-0 glass"></div>

            {/* Content */}
            <div className="relative z-10 text-center py-16 px-8">
              <h2 className="text-3xl md:text-4xl font-bold mb-4">
                Ready to Start Your <span className="text-brand">Journey</span>?
              </h2>
              <p className="text-slate-300 text-lg max-w-xl mx-auto mb-8">
                Join thousands of developers who have mastered microservices architecture with our comprehensive course.
              </p>
              <a href="/course" className="btn-primary text-lg px-8 py-4 inline-flex">
                <span>Start Learning Now</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </a>
            </div>
          </div>
        </div>
      </section>

      <Footer />
    </>
  );
}
